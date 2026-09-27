import { LogOut, PenLine, User as UserIcon } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { Avatar } from "@/components/ui/Avatar";
import { buttonVariants } from "@/components/ui/buttonVariants";
import { useAuthStore } from "@/store/auth";

export function UserMenu() {
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const logout = useAuthStore((s) => s.logout);
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  if (!isAuthenticated || !user) {
    return (
      <div className="flex items-center gap-2">
        <Link to="/login" className={buttonVariants({ variant: "ghost", size: "sm" })}>
          Log in
        </Link>
        <Link to="/register" className={buttonVariants({ size: "sm" })}>
          Sign up
        </Link>
      </div>
    );
  }

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-2 rounded-full p-0.5 transition-colors hover:bg-muted-bg"
        aria-label="Account menu"
      >
        <Avatar name={user.username} src={user.avatar} className="size-9" />
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-56 origin-top-right rounded-xl border border-border bg-card p-1.5 shadow-[var(--shadow)] animate-fade-in-up">
          <div className="border-b border-border px-3 py-2">
            <p className="truncate text-sm font-semibold text-foreground">
              {user.username}
            </p>
            <p className="truncate text-xs text-muted">{user.email}</p>
          </div>
          <MenuLink to={`/u/${user.username}`} icon={UserIcon} onClick={() => setOpen(false)}>
            Profile
          </MenuLink>
          <MenuLink to="/new" icon={PenLine} onClick={() => setOpen(false)}>
            Write an article
          </MenuLink>
          <button
            onClick={() => {
              logout();
              setOpen(false);
              navigate("/");
            }}
            className="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-sm text-danger transition-colors hover:bg-muted-bg"
          >
            <LogOut className="size-4" />
            Log out
          </button>
        </div>
      )}
    </div>
  );
}

function MenuLink({
  to,
  icon: Icon,
  children,
  onClick,
}: {
  to: string;
  icon: typeof UserIcon;
  children: React.ReactNode;
  onClick: () => void;
}) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className="flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm text-foreground transition-colors hover:bg-muted-bg"
    >
      <Icon className="size-4 text-muted" />
      {children}
    </Link>
  );
}
