import { Link, useParams, useSearchParams } from "react-router-dom";

import { useDiff } from "@/api/revisions";
import { DiffViewer } from "@/components/history/DiffViewer";
import { RailGroup, Sidebar } from "@/components/layout/Sidebar";
import { WikiFrame } from "@/components/layout/WikiFrame";
import { EmptyState } from "@/components/ui/EmptyState";
import { Skeleton } from "@/components/ui/Skeleton";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import { apiErrorMessage } from "@/lib/api";
import type { DiffPayload, DiffSide } from "@/lib/types";
import { formatBytes, formatDateTime } from "@/lib/utils";

/**
 * `/wiki/:slug/diff?from=&to=` — DECISIONS §14 fixes this route and its two
 * query parameters, and they map straight onto the API's own
 * `GET /api/articles/{slug}/diff/?from=&to=`.
 *
 * Both ends are optional, and each omission means something precise:
 * `to` absent is "the current revision", `from` absent is "the revision before
 * `to`", and `from=0` is the page-creation diff against the empty document.
 * That is what lets every entry point — the history form, a `cur` / `prev`
 * link, a Recent-changes row, an RSS item — build a URL without first looking
 * anything up.
 *
 * `noindex`, like Search: a diff is a view of two internal ids, it has no
 * stable meaning to a crawler, and there are `revision_count²` of them.
 */
export function DiffPage() {
  const { slug = "" } = useParams();
  const [params] = useSearchParams();

  const from = revisionRef(params.get("from"));
  const to = revisionRef(params.get("to"));
  const { data: diff, isLoading, isError, error } = useDiff(slug, from, to);

  const title = diff?.article.title ?? slug;
  const heading = `Difference between revisions of ${title}`;

  useDocumentMeta({
    title: heading,
    description: `A comparison of two revisions of the Wikiverse article ${title}.`,
    robots: "noindex",
    canonical: `/wiki/${slug}/diff`,
  });

  return (
    <WikiFrame rail={<Sidebar />} tools={<Tools slug={slug} />}>
      <div className="pt-4 pb-3">
        <h1 className="font-serif text-h1 font-normal text-ink text-balance">
          {heading}
        </h1>
        <hr className="mt-1.5 border-0 border-t border-rule" />
        <p className="mt-1.5 text-ui text-ink-2">
          <Link to={`/wiki/${slug}`} className="text-link hover:underline">
            {title}
          </Link>
          {" · "}
          <Link
            to={`/wiki/${slug}/history`}
            className="text-link hover:underline"
          >
            Revision history
          </Link>
        </p>
      </div>

      {isError ? (
        <EmptyState
          title="This comparison could not be loaded."
          hint={
            <>
              {apiErrorMessage(
                error,
                "One or both of those revisions do not exist.",
              )}{" "}
              <Link
                to={`/wiki/${slug}/history`}
                className="text-link hover:underline"
              >
                Pick two revisions from the history
              </Link>
              .
            </>
          }
        />
      ) : isLoading || !diff ? (
        <DiffSkeleton />
      ) : (
        <>
          <Heads diff={diff} slug={slug} />
          <DiffViewer diff={diff} />
        </>
      )}
    </WikiFrame>
  );
}

/* ---------------------------------------------------------------------------
   The two comparison heads
   ------------------------------------------------------------------------- */

function Heads({ diff, slug }: { diff: DiffPayload; slug: string }) {
  return (
    <div className="mt-4 grid gap-3 shelf:grid-cols-2">
      <Head
        id="diff-older"
        label="Older revision"
        side={diff.from_revision}
        step={
          diff.from_revision.id === null
            ? null
            : {
                to: `/wiki/${slug}/diff?to=${diff.from_revision.id}`,
                text: "← Previous edit",
              }
        }
      />
      <Head
        id="diff-newer"
        label="Newer revision"
        side={diff.to_revision}
        step={
          diff.next_id === null
            ? null
            : { to: `/wiki/${slug}/diff?to=${diff.next_id}`, text: "Newer edit →" }
        }
      />
    </div>
  );
}

interface HeadProps {
  id: string;
  label: string;
  side: DiffSide;
  step: { to: string; text: string } | null;
}

/**
 * One side of the comparison, as a named region so a screen-reader user can
 * jump straight to "Newer revision" instead of walking the whole header.
 *
 * The page-creation side carries `id: null` and every other field empty. It is
 * rendered as a sentence rather than as a row of blanks, because "the article
 * did not exist" is information, not missing data.
 */
function Head({ id, label, side, step }: HeadProps) {
  const empty = side.id === null;

  return (
    <section
      aria-labelledby={id}
      className="border border-rule-hair bg-panel px-3 py-2 text-ui"
    >
      <h2
        id={id}
        className="text-2xs font-semibold tracking-[0.06em] text-ink-2 uppercase"
      >
        {label}
      </h2>

      {empty ? (
        <p className="mt-1 text-ink">
          The empty document — this comparison shows the article being created.
        </p>
      ) : (
        <>
          <p className="mt-1 text-ink">
            Revision as of{" "}
            <time dateTime={side.created_at ?? undefined} className="tabular-nums">
              {side.created_at ? formatDateTime(side.created_at) : "an unknown date"}
            </time>
          </p>

          <p className="mt-0.5 text-ink-2">
            {side.editor ? (
              <Link
                to={`/u/${side.editor.username}`}
                className="text-link hover:underline"
              >
                {side.editor.username}
              </Link>
            ) : (
              <span className="text-ink-3">anonymous</span>
            )}
            {side.byte_size !== null && (
              <>
                {" · "}
                <span className="tabular-nums">{formatBytes(side.byte_size)}</span>
              </>
            )}
            {side.is_minor && (
              <>
                {" · "}
                <abbr title="Minor edit" className="text-flag font-bold text-ink no-underline">
                  <span aria-hidden="true">m</span>
                  <span className="sr-only">minor edit</span>
                </abbr>
              </>
            )}
          </p>

          <p className="mt-0.5 italic text-ink-2">
            {side.comment || "No edit summary"}
          </p>
        </>
      )}

      <p className="mt-1">
        {step ? (
          <Link to={step.to} className="text-link hover:underline">
            {step.text}
          </Link>
        ) : (
          <span className="text-ink-3">
            {empty ? "No earlier revision" : "This is the current revision"}
          </span>
        )}
      </p>
    </section>
  );
}

/* ---------------------------------------------------------------------------
   Params and loading
   ------------------------------------------------------------------------- */

/**
 * A revision reference from the URL.
 *
 * `0` is meaningful — it is the page-creation diff — so it is kept, while an
 * absent, blank or unparseable value becomes `null` and lets the server apply
 * its own default. A hand-edited `?from=abc` therefore renders the default
 * comparison instead of a 400.
 */
function revisionRef(raw: string | null): number | null {
  if (raw === null || raw.trim() === "") return null;
  const value = Number(raw);
  return Number.isSafeInteger(value) && value >= 0 ? value : null;
}

function Tools({ slug }: { slug: string }) {
  return (
    <nav aria-label="Tools" className="text-ui">
      <h2 className="border-b border-rule-hair px-2 pb-1 text-2xs font-semibold tracking-[0.06em] text-ink-2 uppercase">
        Tools
      </h2>
      <RailGroup>
        <li>
          <Link to={`/wiki/${slug}`} className={TOOL_LINK}>
            Read the article
          </Link>
        </li>
        <li>
          <Link to={`/wiki/${slug}/history`} className={TOOL_LINK}>
            Revision history
          </Link>
        </li>
        <li>
          <Link to={`/wiki/${slug}/edit`} className={TOOL_LINK}>
            Edit this article
          </Link>
        </li>
      </RailGroup>
    </nav>
  );
}

const TOOL_LINK =
  "block rounded-chrome px-2 py-1 text-link transition-colors duration-100 hover:bg-panel hover:text-link-hover motion-reduce:transition-none";

function DiffSkeleton() {
  return (
    <div aria-busy="true">
      <div className="mt-4 grid gap-3 shelf:grid-cols-2">
        <Skeleton className="h-28 w-full" />
        <Skeleton className="h-28 w-full" />
      </div>
      <div className="mt-4 space-y-1">
        {Array.from({ length: 10 }, (_, index) => (
          <Skeleton key={index} className="h-6 w-full" />
        ))}
      </div>
      <span className="sr-only">Loading the comparison…</span>
    </div>
  );
}
