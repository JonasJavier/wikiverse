import { Link } from "react-router-dom";

import type { MainPageStats } from "@/api/mainpage";
import { formatNumber } from "@/lib/utils";

interface SiteStatisticsProps {
  stats: MainPageStats | undefined;
  className?: string;
}

/**
 * Site statistics as ONE SENTENCE, not four KPI tiles.
 *
 * The tiles were the most SaaS-looking element on the old home page: four
 * boxes, four icons, four tinted circles, to carry four integers that read
 * perfectly well in a line of prose. A sentence is also the honest place to
 * put the contribution invitation, which replaces the solid-indigo call to
 * action entirely — the last clause is the only ask on the page.
 *
 * Every figure is tabular (the app-wide default, §6.3) so the numbers align
 * with the counts in the panels above.
 */
export function SiteStatistics({ stats, className }: SiteStatisticsProps) {
  if (!stats) return null;

  return (
    <p className={className}>
      Wikiverse has <Figure value={stats.articles} /> article
      {stats.articles === 1 ? "" : "s"}, <Figure value={stats.revisions} /> revision
      {stats.revisions === 1 ? "" : "s"}, <Figure value={stats.categories} /> categor
      {stats.categories === 1 ? "y" : "ies"} and <Figure value={stats.contributors} />{" "}
      contributor{stats.contributors === 1 ? "" : "s"}
      {typeof stats.words === "number" && stats.words > 0 && (
        <>
          , totalling <Figure value={stats.words} /> words
        </>
      )}
      .{" "}
      <Link to="/new" className="text-link hover:underline">
        You can help by writing one
      </Link>
      .
    </p>
  );
}

function Figure({ value }: { value: number }) {
  return <span className="tabular-nums text-ink">{formatNumber(value)}</span>;
}
