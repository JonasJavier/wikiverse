import { type ReactNode, useState } from "react";
import { Link } from "react-router-dom";

import {
  useCreateTalkMessage,
  useDeleteTalkMessage,
  useUpdateTalkMessage,
} from "@/api/community";
import { Markdown } from "@/components/article/Markdown";
import { TalkComposer } from "@/components/community/TalkComposer";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { apiErrorMessage } from "@/lib/api";
import type { TalkMessage as TalkMessageData } from "@/lib/types";
import { cn, formatDateTime } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";
import { toast } from "@/store/toast";

/**
 * One comment, its signature, and its own replies.
 *
 * THE PERMISSION RULES, mirroring `permissions.py` exactly so the UI never
 * offers a control the server will refuse:
 *
 *   - **Reply** — `CanPostToTalk`: any signed-in reader, unless the thread is
 *     locked, in which case staff only. A deleted comment offers no reply
 *     affordance: the node survives so the thread still reads, not so the
 *     conversation can continue under a tombstone.
 *   - **Edit / Delete** — `IsMessageAuthorOrStaff`: your own comment, or
 *     anybody's if you are staff. A comment that is already deleted is closed
 *     to non-staff, so its author sees no controls either.
 *
 * Deletion is SOFT. The row stays, replies are not orphaned, and the audit
 * trail survives; the serializer withholds `body` from non-staff afterwards,
 * so this renders a tombstone rather than an empty bubble. Staff see the text
 * with a notice saying why they can.
 *
 * `id="c-{id}"` makes every comment linkable, and the timestamp is its own
 * permalink — the anchor Recent changes points a talk row at.
 */

export interface TalkMessageProps {
  slug: string;
  threadId: number;
  message: TalkMessageData;
  /** `TalkThread.is_locked`. Only staff may post to a locked thread. */
  locked: boolean;
  /** Nested replies, already built into a tree by `TalkThread`. */
  children?: ReactNode;
}

export function TalkMessage({
  slug,
  threadId,
  message,
  locked,
  children,
}: TalkMessageProps) {
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  const [replying, setReplying] = useState(false);
  const [editing, setEditing] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  const reply = useCreateTalkMessage(slug);
  const update = useUpdateTalkMessage(slug);
  const remove = useDeleteTalkMessage(slug);

  const isOwn = Boolean(user && message.author && user.id === message.author.id);
  const isStaff = Boolean(user?.is_staff);
  const canModify = isStaff || (isOwn && !message.is_deleted);
  const canReply =
    isAuthenticated && !message.is_deleted && (!locked || isStaff);

  const anchor = `c-${message.id}`;

  return (
    <li id={anchor} className="py-2">
      {message.is_deleted && (
        <p className="text-ui text-ink-3 italic">
          This comment was removed.
          {isStaff && message.body !== null && (
            <span className="not-italic">
              {" "}
              Its text is shown below because you are staff.
            </span>
          )}
        </p>
      )}

      {editing ? (
        <TalkComposer
          submitLabel="Save changes"
          initialBody={message.body ?? ""}
          autoFocus
          busy={update.isPending}
          note="Editing does not hide the original from the page history."
          onCancel={() => setEditing(false)}
          onSubmit={({ body }) =>
            update.mutate(
              { id: message.id, threadId, body },
              {
                onSuccess: () => {
                  setEditing(false);
                  toast.success("Comment updated.");
                },
                onError: (error) =>
                  toast.error("Could not save that edit.", {
                    detail: apiErrorMessage(error),
                  }),
              },
            )
          }
        />
      ) : (
        message.body !== null && (
          /* `headings={false}`: a `##` inside a comment must not mint a
             heading id, because those ids would collide with the thread
             anchors (`#thread-N`) and with each other across comments, and a
             hover `#` permalink inside somebody's reply points at nothing
             stable. Wikilinks, red links and footnote markers still resolve —
             this is the same renderer an article body uses. */
          <Markdown content={message.body} headings={false} />
        )
      )}

      {!editing && (
        <p className="mt-1 flex flex-wrap items-baseline gap-x-2 gap-y-0.5 text-2xs text-ink-2">
          {message.author ? (
            <Link
              to={`/u/${message.author.username}`}
              className="font-medium text-link hover:underline"
            >
              {message.author.username}
            </Link>
          ) : (
            <span className="italic">{message.is_deleted ? "author withheld" : "account removed"}</span>
          )}

          <a href={`#${anchor}`} className="text-link tabular-nums hover:underline">
            <time dateTime={message.created_at}>
              {formatDateTime(message.created_at)}
            </time>
          </a>

          {message.edited_at && (
            <span title={formatDateTime(message.edited_at)}>(edited)</span>
          )}

          {canReply && (
            <SigButton
              expanded={replying}
              onClick={() => setReplying((value) => !value)}
            >
              reply
            </SigButton>
          )}
          {canModify && (
            <SigButton onClick={() => setEditing(true)}>edit</SigButton>
          )}
          {canModify && !message.is_deleted && (
            <SigButton onClick={() => setConfirmDelete(true)}>delete</SigButton>
          )}
        </p>
      )}

      {replying && (
        <TalkComposer
          submitLabel="Post reply"
          autoFocus
          busy={reply.isPending}
          className="mt-2"
          note="Your name and the time are added automatically."
          onCancel={() => setReplying(false)}
          onSubmit={({ body }) =>
            reply.mutate(
              { threadId, body, parent: message.id },
              {
                onSuccess: () => setReplying(false),
                onError: (error) =>
                  toast.error("Could not post that reply.", {
                    detail: apiErrorMessage(error),
                  }),
              },
            )
          }
        />
      )}

      {children}

      <ConfirmDialog
        open={confirmDelete}
        title="Remove this comment?"
        tone="danger"
        confirmLabel="Remove comment"
        busy={remove.isPending}
        body={
          <p>
            The comment is struck from the page but the row is kept, so replies
            to it are not orphaned and the discussion still reads. Staff can
            still see the text.
          </p>
        }
        onCancel={() => setConfirmDelete(false)}
        onConfirm={() =>
          remove.mutate(
            { id: message.id, threadId },
            {
              onSuccess: () => {
                setConfirmDelete(false);
                toast.success("Comment removed.");
              },
              onError: (error) => {
                setConfirmDelete(false);
                toast.error("Could not remove that comment.", {
                  detail: apiErrorMessage(error),
                });
              },
            },
          )
        }
      />
    </li>
  );
}

/**
 * A signature-line action. It is a real `<button>` at 12px, never an `<a>`
 * with no href — the thing that looks like a link and does nothing under
 * Enter is the classic wiki-clone accessibility defect.
 */
function SigButton({
  expanded,
  onClick,
  children,
}: {
  expanded?: boolean;
  onClick: () => void;
  children: ReactNode;
}) {
  return (
    <button
      type="button"
      aria-expanded={expanded}
      onClick={onClick}
      className={cn(
        "cursor-pointer rounded-chrome text-link hover:underline",
        expanded && "font-semibold",
      )}
    >
      {children}
    </button>
  );
}
