import { Eye, LogOut, PenLine, User as UserIcon } from "lucide-react";
import { type KeyboardEvent, type ReactNode, useEffect, useRef, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { useLogout } from "@/api/auth";
import { Avatar } from "@/components/ui/Avatar";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";

/**
 * Signed out: two text links. Signed in: an avatar button opening a menu.
 *
 * The menu follows the menu-button pattern: `aria-haspopup`, `aria-expanded`,
 * Escape closes it and returns focus to the button, arrow keys move between
 * items, and a click outside closes it. Log out goes through `useLogout()` so
 * the refresh token is blacklisted server-side before the session is dropped
 * (DECISIONS §7.2).
 */
export function UserMenu() {
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const logout = useLogout();
  const navigate = useNavigate();
  const location = useLocation();
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => setOpen(false), [location.pathname]);

  useEffect(() => {
    if (!open) return;
    function onPointerDown(event: PointerEvent) {
      if (rootRef.current && !rootRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("pointerdown", onPointerDown);
    // Move focus into the menu so the arrow keys work immediately.
    menuRef.current?.querySelector<HTMLElement>("[role=menuitem]")?.focus();
    return () => document.removeEventListener("pointerdown", onPointerDown);
  }, [open]);

  if (!isAuthenticated || !user) {
    // Router state, as `ProtectedRoute` does: `LoginPage` returns the reader
    // here afterwards, and nothing user-controlled ever lands in the URL.
    const from = `${location.pathname}${location.search}${location.hash}`;
    return (
      <div className="flex items-center gap-3 pl-1 text-ui">
        <Link to="/login" state={{ from }} className="text-link hover:text-link-hover">
          Log in
        </Link>
        <Link
          to="/register"
          className="hidden text-link hover:text-link-hover sm:inline"
        >
          Create account
        </Link>
      </div>
    );
  }

  function close() {
    setOpen(false);
    buttonRef.current?.focus();
  }

  function onMenuKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    const items = Array.from(
      menuRef.current?.querySelectorAll<HTMLElement>("[role=menuitem]") ?? [],
    );
    const index = items.indexOf(document.activeElement as HTMLElement);
    if (event.key === "Escape") {
      event.preventDefault();
      close();
    } else if (event.key === "ArrowDown") {
      event.preventDefault();
      items[(index + 1) % items.length]?.focus();
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      items[(index - 1 + items.length) % items.length]?.focus();
    } else if (event.key === "Tab") {
      setOpen(false);
    }
  }

  return (
    <div className="relative" ref={rootRef}>
      <button
        ref={buttonRef}
        type="button"
        onClick={() => setOpen((value) => !value)}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label={`Account menu for ${user.username}`}
        className="grid size-8 place-items-center rounded-full hover:bg-panel"
      >
        <Avatar name={user.username} src={user.avatar} className="size-7" />
      </button>

      {open && (
        <div
          ref={menuRef}
          role="menu"
          aria-label="Account"
          onKeyDown={onMenuKeyDown}
          className="absolute right-0 z-50 mt-1 w-56 rounded-chrome border border-rule bg-page py-1 shadow-[var(--shadow-dialog)]"
        >
          <div className="border-b border-rule-hair px-3 py-2">
            <p className="truncate text-ui font-semibold text-ink">{user.username}</p>
            {user.email && <p className="truncate text-2xs text-ink-2">{user.email}</p>}
          </div>
          <MenuLink to={`/u/${user.username}`} icon={<UserIcon />}>
            Profile and contributions
          </MenuLink>
          <MenuLink to="/watchlist" icon={<Eye />}>
            Watchlist
          </MenuLink>
          <MenuLink to="/new" icon={<PenLine />}>
            Create an article
          </MenuLink>
          <button
            type="button"
            role="menuitem"
            tabIndex={-1}
            disabled={logout.isPending}
            onClick={() => {
              logout.mutate(undefined, {
                onSettled: () => {
                  setOpen(false);
                  navigate("/");
                },
              });
            }}
            className="flex w-full items-center gap-2.5 border-t border-rule-hair px-3 py-2 text-left text-ui text-ink hover:bg-panel focus:bg-panel focus:outline-none"
          >
            <LogOut className="size-4 text-ink-2" aria-hidden="true" />
            Log out
          </button>
        </div>
      )}
    </div>
  );
}

function MenuLink({
  to,
  icon,
  children,
}: {
  to: string;
  icon: ReactNode;
  children: ReactNode;
}) {
  return (
    <Link
      to={to}
      role="menuitem"
      tabIndex={-1}
      className={cn(
        "flex items-center gap-2.5 px-3 py-2 text-ui text-ink hover:bg-panel focus:bg-panel focus:outline-none",
        "[&>svg]:size-4 [&>svg]:text-ink-2",
      )}
    >
      {icon}
      {children}
    </Link>
  );
}
