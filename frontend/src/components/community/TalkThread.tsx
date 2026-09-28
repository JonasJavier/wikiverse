import { Link2, Lock } from "lucide-react";
import type { ReactNode } from "react";

import {
  type TalkThreadListItem,
  useCreateTalkMessage,
  useTalkThread,
} from "@/api/community";
import { TalkComposer } from "@/components/community/TalkComposer";
import { TalkMessage } from "@/components/community/TalkMessage";
import { Badge } from "@/components/ui/Badge";
import { Skeleton } from "@/components/ui/Skeleton";
import { apiErrorMessage } from "@/lib/api";
import type { TalkMessage as TalkMessageData } from "@/lib/types";
import { formatDateTime, formatNumber, formatRelativeTime } from "@/lib/utils";
import { toast } from "@/store/toast";

/**
 * One discussion topic: heading, metadata line, the reply tree, a composer.
 *
 * **There is no Subscribe button.** DECISIONS §12 cut it: no subscription
 * model exists behind it, and a dead button is worse than no button. The
 * metadata line therefore ends at the participant count, which is the part
 * that is real.
 *
 * The thread list endpoint does not embed messages, so each thread loads its
 * own detail. The nesting is a `<ul>` of `<li>`, not design-ui §4.13's
 * `<dl>/<dd>`: a description list containing no `<dt>` is invalid HTML and
 * announces as "description list, 4 items" with no terms, which is a worse
 * answer for a conversation than a plain nested list. The measured Wikipedia
 * indent is kept exactly — 1.6rem per level — and the hairline left rule per
 * level is this design's addition, because indentation alone stops being
 * readable at depth 4 (which is where the backend caps it).
 */

export interface TalkThreadProps {
  slug: string;
  thread: TalkThreadListItem;
}

export function TalkThread({ slug, thread }: TalkThreadProps) {
  const detail = useTalkThread(thread.id);
  const post = useCreateTalkMessage(slug);

  const anchor = `thread-${thread.id}`;
  const messages = detail.data?.messages ?? [];
  const messageCount = detail.data?.message_count ?? thread.message_count;
  const participantCount =
    detail.data?.participant_count ?? thread.participant_count;
  const lastActivity = detail.data?.last_message_at ?? thread.last_message_at;
  const locked = detail.data?.is_locked ?? thread.is_locked;
  const resolved = detail.data?.is_resolved ?? thread.is_resolved;

  return (
    <section
      className="border-t border-rule pt-4 first:border-t-0 first:pt-0"
      aria-labelledby={anchor}
    >
      <h2
        id={anchor}
        className="group flex flex-wrap items-baseline gap-x-2 font-serif text-h2 font-normal text-ink"
      >
        <span>{thread.title}</span>
        {resolved && <Badge>Resolved</Badge>}
        {locked && (
          <Badge>
            <Lock aria-hidden="true" className="mr-1 inline size-3" />
            Locked
          </Badge>
        )}
        <a
          href={`#${anchor}`}
          aria-label={`Permanent link to “${thread.title}”`}
          className="text-ink-3 opacity-0 transition-opacity duration-100 group-hover:opacity-100 focus-visible:opacity-100"
        >
          <Link2 aria-hidden="true" className="size-4" />
        </a>
      </h2>

      <p className="mt-1 text-ui text-ink-2">
        {lastActivity ? (
          <>
            Latest comment{" "}
            <time dateTime={lastActivity} title={formatDateTime(lastActivity)}>
              {formatRelativeTime(lastActivity)}
            </time>
          </>
        ) : (
          "No comments yet"
        )}
        {" · "}
        <span className="tabular-nums">{formatNumber(messageCount)}</span>{" "}
        {messageCount === 1 ? "comment" : "comments"}
        {" · "}
        <span className="tabular-nums">{formatNumber(participantCount)}</span>{" "}
        {participantCount === 1 ? "person" : "people"} in discussion
      </p>

      {detail.isPending ? (
        <div className="mt-3 space-y-2" aria-busy="true">
          <Skeleton className="h-4 w-4/5" />
          <Skeleton className="h-4 w-3/5" />
        </div>
      ) : detail.isError ? (
        <p className="mt-3 text-ui text-ink-2">
          This discussion could not be loaded.
        </p>
      ) : (
        <Replies depth={0}>
          {buildTree(messages).map((node) => (
            <MessageNode
              key={node.message.id}
              node={node}
              slug={slug}
              threadId={thread.id}
              locked={locked}
            />
          ))}
        </Replies>
      )}

      {locked ? (
        <p className="mt-3 rounded-chrome border border-rule-hair bg-panel px-3 py-2 text-ui text-ink-2">
          This topic is locked. Only staff can add to it.
        </p>
      ) : (
        <TalkComposer
          // Remounting on the message count is what clears the box after a
          // successful post, without a `useEffect` reaching into a child.
          key={`composer-${thread.id}-${messageCount}`}
          submitLabel="Add comment"
          placeholder="Add to this topic. Markdown is supported; raw HTML is not."
          note="Your name and the time are added automatically."
          busy={post.isPending}
          className="mt-3"
          onSubmit={({ body }) =>
            post.mutate(
              { threadId: thread.id, body, parent: null },
              {
                onError: (error) =>
                  toast.error("Could not post that comment.", {
                    detail: apiErrorMessage(error),
                  }),
              },
            )
          }
        />
      )}
    </section>
  );
}

/* ---------------------------------------------------------------------
   The reply tree
   --------------------------------------------------------------------- */

interface ReplyNode {
  message: TalkMessageData;
  children: ReplyNode[];
}

/**
 * Flat list to tree, in one pass plus one ordering pass.
 *
 * A message whose parent is not in this thread's payload (it cannot normally
 * happen, but a hand-rolled API call could produce it) is promoted to the top
 * level rather than dropped: losing a comment is a worse failure than showing
 * one at the wrong indent.
 */
function buildTree(messages: TalkMessageData[]): ReplyNode[] {
  const nodes = new Map<number, ReplyNode>();
  for (const message of messages) {
    nodes.set(message.id, { message, children: [] });
  }

  const roots: ReplyNode[] = [];
  for (const message of messages) {
    const node = nodes.get(message.id);
    if (!node) continue;
    const parent = message.parent === null ? undefined : nodes.get(message.parent);
    if (parent) {
      parent.children.push(node);
    } else {
      roots.push(node);
    }
  }

  return roots;
}

function MessageNode({
  node,
  slug,
  threadId,
  locked,
}: {
  node: ReplyNode;
  slug: string;
  threadId: number;
  locked: boolean;
}) {
  return (
    <TalkMessage
      slug={slug}
      threadId={threadId}
      message={node.message}
      locked={locked}
    >
      {node.children.length > 0 && (
        <Replies depth={node.message.depth + 1}>
          {node.children.map((child) => (
            <MessageNode
              key={child.message.id}
              node={child}
              slug={slug}
              threadId={threadId}
              locked={locked}
            />
          ))}
        </Replies>
      )}
    </TalkMessage>
  );
}

/**
 * 1.6rem indent per level — Wikipedia's measured 25.6px — plus a hairline
 * left rule so the structure survives the deepest level the backend allows.
 */
function Replies({ depth, children }: { depth: number; children: ReactNode }) {
  return (
    <ul
      className={
        depth === 0
          ? "mt-2 divide-y divide-rule-hair"
          : "mt-1 ml-[1.6rem] border-l border-rule-hair pl-[0.9rem]"
      }
    >
      {children}
    </ul>
  );
}
