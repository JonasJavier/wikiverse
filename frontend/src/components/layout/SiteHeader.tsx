import { Activity, Menu, Search, Shuffle, X } from "lucide-react";
import { type ReactNode, useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";

import { useIsShelf } from "@/hooks/useMediaQuery";
import { cn } from "@/lib/utils";
import { Logo } from "./Logo";
import { SidebarLinks } from "./Sidebar";
import { ThemeToggle } from "./ThemeToggle";
import { TypeaheadSearch } from "./TypeaheadSearch";
import { UserMenu } from "./UserMenu";

/**
 * The masthead (design-ui §3.4) — the rewrite of the old `Navbar`.
 *
 * Not sticky, no blur, no shadow: a rule under the shell colour. Below `shelf`
 * the left rail does not exist, so the hamburger opens the same site navigation
 * as a disclosure panel under the bar. On a phone the search box gives way to a
 * search icon that opens the full search page, where the input has room.
 */
export function SiteHeader() {
  const isShelf = useIsShelf();
  const location = useLocation();
  const [open, setOpen] = useState(false);

  // Close the panel on navigation and when the viewport grows past `shelf`,
  // where the rail takes over and the toggle disappears.
  useEffect(() => setOpen(false), [location.pathname]);
  useEffect(() => {
    if (isShelf) setOpen(false);
  }, [isShelf]);

  return (
    <header className="border-b border-rule bg-shell print:hidden">
      <div className="mx-auto flex h-14 max-w-[81.5rem] items-center gap-3 px-4 sm:px-6 tools:px-8">
        <button
          type="button"
          className="-ml-1 grid size-9 shrink-0 place-items-center rounded-chrome text-ink hover:bg-panel shelf:hidden"
          aria-label="Site navigation"
          aria-expanded={open}
          aria-controls="site-nav-panel"
          onClick={() => setOpen((value) => !value)}
        >
          {open ? (
            <X className="size-5" aria-hidden="true" />
          ) : (
            <Menu className="size-5" aria-hidden="true" />
          )}
        </button>

        <Logo />

        <TypeaheadSearch className="mx-auto hidden w-full max-w-[28rem] sm:block" />

        <nav aria-label="User" className="ml-auto flex shrink-0 items-center gap-1 sm:ml-0">
          <IconLink to="/search" label="Search" className="sm:hidden">
            <Search className="size-4" aria-hidden="true" />
          </IconLink>
          <IconLink to="/random" label="Random article">
            <Shuffle className="size-4" aria-hidden="true" />
          </IconLink>
          <IconLink to="/changes" label="Recent changes" className="hidden shelf:grid">
            <Activity className="size-4" aria-hidden="true" />
          </IconLink>
          <ThemeToggle />
          <UserMenu />
        </nav>
      </div>

      {open && !isShelf && (
        <div
          id="site-nav-panel"
          className="border-t border-rule-hair bg-shell px-4 pt-3 pb-4 sm:px-6"
        >
          <nav aria-label="Site">
            <SidebarLinks onNavigate={() => setOpen(false)} />
          </nav>
        </div>
      )}
    </header>
  );
}

function IconLink({
  to,
  label,
  className,
  children,
}: {
  to: string;
  label: string;
  className?: string;
  children: ReactNode;
}) {
  return (
    <Link
      to={to}
      aria-label={label}
      title={label}
      className={cn(
        "grid size-8 place-items-center rounded-chrome text-ink-2 hover:bg-panel hover:text-ink",
        className,
      )}
    >
      {children}
    </Link>
  );
}
