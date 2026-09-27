/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL of the DRF API, including the `/api` prefix. */
  readonly VITE_API_URL?: string;
  /**
   * Public origin of the deployed site, e.g. `https://wikiverse.example.dev`.
   * Used to emit an absolute `<link rel="canonical">` and `og:url`, so a
   * preview deploy does not advertise itself as canonical. Falls back to
   * `window.location.origin`.
   */
  readonly VITE_PUBLIC_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
