import { Link } from "react-router-dom";

import { buttonVariants } from "@/components/ui/buttonVariants";

export function NotFoundPage() {
  return (
    <div className="mx-auto flex max-w-lg flex-col items-center px-4 py-28 text-center">
      <p className="font-serif text-7xl font-bold text-primary">404</p>
      <h1 className="mt-4 font-serif text-2xl font-bold text-foreground">
        Page not found
      </h1>
      <p className="mt-2 text-muted">
        The page you&apos;re looking for doesn&apos;t exist or has been moved.
      </p>
      <div className="mt-6 flex gap-3">
        <Link to="/" className={buttonVariants()}>
          Go home
        </Link>
        <Link to="/browse" className={buttonVariants({ variant: "outline" })}>
          Browse articles
        </Link>
      </div>
    </div>
  );
}
