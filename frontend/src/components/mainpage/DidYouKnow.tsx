import type { LinkResolver } from "@/components/article/markdownUtils";
import { WikiText } from "./WikiText";

interface DidYouKnowProps {
  /**
   * Full hook SENTENCES from `GET /api/main-page/` — NOT article titles. Each
   * one is markdown that conventionally begins "… that" and ends in "?", and
   * carries one bolded wikilink.
   */
  hooks: string[];
  /** The shared existence oracle, so a hook's wikilink can go red. */
  resolve?: LinkResolver;
}

/**
 * Did you know… — a bulleted list of hooks.
 *
 * The bullet is a real `ul` marker rather than a drawn dot, because this list
 * is the one place on the front page where the content is a set of loose facts
 * and the disc is the convention that says so. The em-dash-leading "… that"
 * phrasing comes from the data, not from here: the panel must not manufacture
 * it, or an editor who writes a plain sentence gets a broken one.
 */
export function DidYouKnow({ hooks, resolve }: DidYouKnowProps) {
  if (hooks.length === 0) {
    return (
      <p className="text-ui text-ink-2">
        No hooks have been written yet. They are editorial blocks, added through
        the admin.
      </p>
    );
  }

  return (
    <ul className="list-disc space-y-1.5 pl-5 font-serif text-read leading-[1.55] text-ink marker:text-ink-3">
      {hooks.map((hook, index) => (
        <li key={index}>
          <WikiText resolve={resolve}>{hook}</WikiText>
        </li>
      ))}
    </ul>
  );
}
