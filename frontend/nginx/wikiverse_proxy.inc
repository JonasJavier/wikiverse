# Shared proxy settings for every backend location.
#
# Included from nginx.conf.template. envsubst does NOT process this file, so it
# must contain no ${...} placeholders -- the two deployment-specific values
# arrive as the nginx variables $wikiverse_backend_host (set by a map in the
# template) and the proxy_pass target written at each call site.

proxy_http_version 1.1;

# Railway terminates TLS and routes by SNI + Host, so both have to name the
# backend rather than the browser's original host.
proxy_ssl_server_name on;
proxy_set_header Host $wikiverse_backend_host;

proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Forwarded-Host $host;

# Do not rewrite Location headers: Django already builds absolute URLs from
# PUBLIC_BASE_URL, and rewriting them here would point at the backend host.
proxy_redirect off;

proxy_connect_timeout 15s;
proxy_send_timeout 60s;
# Generous: Railway sleeps idle services, so the first request after a quiet
# period pays a cold start of several seconds.
proxy_read_timeout 60s;

proxy_buffering on;
proxy_buffers 16 16k;
proxy_busy_buffers_size 32k;
