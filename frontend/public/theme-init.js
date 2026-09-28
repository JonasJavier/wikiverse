/*
 * Paint the reader's theme before the first frame.
 *
 * Loaded as a blocking, same-origin script from <head> — an inline script would
 * be refused by the Content Security Policy (script-src 'self'). It mirrors
 * store/theme.ts: the persisted choice is "light", "dark" or "system", and
 * "system" follows prefers-color-scheme. The store takes over once React runs.
 */
(function () {
  var choice = "system";
  try {
    var raw = localStorage.getItem("wikiverse.theme");
    var state = raw ? JSON.parse(raw).state : null;
    if (state && (state.choice || state.theme)) choice = state.choice || state.theme;
  } catch (e) {
    /* Blocked or malformed storage: follow the system. */
  }
  var dark =
    choice === "dark" ||
    (choice !== "light" &&
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches);
  var root = document.documentElement;
  if (dark) root.classList.add("dark");
  root.style.colorScheme = dark ? "dark" : "light";
})();
