// Article pages: the SPA for people, the Open Graph shell for link-preview bots.
//
// Social crawlers do not execute JavaScript, so they would only ever see the
// site-level card baked into index.html. This sends just those user agents to
// the backend's /og/wiki/<slug>/ document; everyone else, Googlebot included
// (it renders JS), falls through to the SPA. Port of the $wikiverse_crawler map
// in frontend/nginx.conf.template.
//
// Runs on Netlify Edge (Deno), outside the Vite build and its tsconfig.

const BACKEND_ORIGIN = "https://wikiverse-api.onrender.com";

const CRAWLER =
  /facebookexternalhit|Twitterbot|Slackbot|LinkedInBot|WhatsApp|TelegramBot|Discordbot|Pinterest|redditbot|Applebot|SkypeUriPreview|embedly|quora link preview|vkShare|W3C_Validator/i;

// Only the bare article URL; /wiki/<slug>/history and friends stay with the SPA.
const ARTICLE = /^\/wiki\/([^/]+)\/?$/;

export default async function ogCrawler(request: Request): Promise<Response | undefined> {
  const match = ARTICLE.exec(new URL(request.url).pathname);
  if (!match || !CRAWLER.test(request.headers.get("user-agent") ?? "")) {
    return undefined;
  }
  return fetch(`${BACKEND_ORIGIN}/og/wiki/${match[1]}/`, {
    headers: { "user-agent": request.headers.get("user-agent") ?? "" },
  });
}

export const config = { path: "/wiki/*" };
