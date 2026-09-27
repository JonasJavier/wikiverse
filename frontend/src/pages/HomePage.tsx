import { ArrowRight, BookOpen, Eye, FolderOpen, Users } from "lucide-react";
import { Link } from "react-router-dom";

import { useArticles, usePopularArticles, useSiteStats } from "@/api/articles";
import { useCategories } from "@/api/categories";
import { ArticleCard } from "@/components/article/ArticleCard";
import { ArticleCardSkeleton } from "@/components/article/ArticleCardSkeleton";
import { CategoryChip } from "@/components/article/CategoryChip";
import { SearchBar } from "@/components/layout/SearchBar";
import { buttonVariants } from "@/components/ui/buttonVariants";
import { formatCount } from "@/lib/utils";

const CONTAINER = "mx-auto max-w-7xl px-4 sm:px-6 lg:px-8";

export function HomePage() {
  const { data: stats } = useSiteStats();
  const { data: popular, isLoading: loadingPopular } = usePopularArticles();
  const { data: recent, isLoading: loadingRecent } = useArticles({
    ordering: "-updated_at",
    page_size: 6,
  });
  const { data: categories } = useCategories();

  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border">
        <div
          className="pointer-events-none absolute inset-0 opacity-[0.07]"
          style={{
            backgroundImage:
              "radial-gradient(circle at 1px 1px, var(--foreground) 1px, transparent 0)",
            backgroundSize: "28px 28px",
          }}
        />
        <div
          className="pointer-events-none absolute -top-40 left-1/2 size-[40rem] -translate-x-1/2 rounded-full opacity-20 blur-3xl"
          style={{ background: "var(--primary)" }}
        />
        <div className={`${CONTAINER} relative py-20 text-center md:py-28`}>
          <span className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1 text-xs font-medium text-muted">
            <span className="size-1.5 rounded-full bg-primary" />
            Free &amp; open knowledge
          </span>
          <h1 className="mx-auto mt-6 max-w-3xl font-serif text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl md:text-6xl">
            The encyclopedia anyone can{" "}
            <span className="text-primary">read &amp; write</span>
          </h1>
          <p className="mx-auto mt-5 max-w-xl text-lg text-muted">
            Explore thousands of articles, contribute your knowledge, and track
            every edit — a modern take on the classic wiki.
          </p>
          <div className="mx-auto mt-8 max-w-xl">
            <SearchBar large autoFocus />
          </div>
          <div className="mt-5 flex flex-wrap items-center justify-center gap-2 text-sm text-muted">
            <span>Popular:</span>
            {categories?.slice(0, 4).map((c) => (
              <CategoryChip key={c.id} category={c} />
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className={`${CONTAINER} -mt-px`}>
        <div className="grid grid-cols-2 divide-x divide-y divide-border overflow-hidden rounded-2xl border border-border md:grid-cols-4 md:divide-y-0">
          <Stat icon={BookOpen} label="Articles" value={stats?.articles} />
          <Stat icon={FolderOpen} label="Categories" value={stats?.categories} />
          <Stat icon={Users} label="Contributors" value={stats?.contributors} />
          <Stat icon={Eye} label="Total views" value={stats?.total_views} />
        </div>
      </section>

      {/* Popular */}
      <section className={`${CONTAINER} mt-16`}>
        <SectionHeader
          title="Trending articles"
          subtitle="The most-read pages right now"
          to="/browse"
        />
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {loadingPopular
            ? Array.from({ length: 6 }).map((_, i) => <ArticleCardSkeleton key={i} />)
            : popular
                ?.slice(0, 6)
                .map((a) => <ArticleCard key={a.id} article={a} />)}
        </div>
      </section>

      {/* Recent */}
      <section className={`${CONTAINER} mt-16`}>
        <SectionHeader
          title="Recently updated"
          subtitle="Fresh edits from the community"
          to="/browse"
        />
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {loadingRecent
            ? Array.from({ length: 6 }).map((_, i) => <ArticleCardSkeleton key={i} />)
            : recent?.results.map((a) => <ArticleCard key={a.id} article={a} />)}
        </div>
      </section>

      {/* CTA */}
      <section className={`${CONTAINER} mt-20`}>
        <div className="relative overflow-hidden rounded-3xl bg-primary px-8 py-14 text-center">
          <h2 className="font-serif text-3xl font-bold text-primary-foreground">
            Share what you know
          </h2>
          <p className="mx-auto mt-3 max-w-md text-primary-foreground/80">
            Every great encyclopedia is built by its readers. Write your first
            article in minutes.
          </p>
          <Link
            to="/new"
            className={`${buttonVariants({ size: "lg" })} mt-6 bg-card text-foreground hover:bg-card`}
          >
            Start writing
            <ArrowRight className="size-4" />
          </Link>
        </div>
      </section>
    </div>
  );
}

function Stat({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof BookOpen;
  label: string;
  value?: number;
}) {
  return (
    <div className="flex items-center gap-3 bg-card p-5">
      <div className="flex size-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
        <Icon className="size-5" />
      </div>
      <div>
        <div className="text-2xl font-bold text-foreground">
          {value === undefined ? "—" : formatCount(value)}
        </div>
        <div className="text-xs text-muted">{label}</div>
      </div>
    </div>
  );
}

function SectionHeader({
  title,
  subtitle,
  to,
}: {
  title: string;
  subtitle: string;
  to: string;
}) {
  return (
    <div className="mb-6 flex items-end justify-between">
      <div>
        <h2 className="font-serif text-2xl font-bold text-foreground">{title}</h2>
        <p className="mt-1 text-sm text-muted">{subtitle}</p>
      </div>
      <Link
        to={to}
        className="flex shrink-0 items-center gap-1 text-sm font-medium text-primary hover:gap-2 transition-all"
      >
        View all
        <ArrowRight className="size-4" />
      </Link>
    </div>
  );
}
