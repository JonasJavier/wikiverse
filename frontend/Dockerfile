# syntax=docker/dockerfile:1

FROM node:22-alpine AS base

WORKDIR /app

COPY package*.json ./

FROM base AS dev

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

FROM base AS build

RUN npm ci

COPY . .

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

FROM nginx:1.27-alpine AS prod

# Rendered by the image entrypoint, which runs envsubst over /etc/nginx/templates.
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
# Not a template: included verbatim, so it must stay free of ${...} placeholders.
COPY nginx/wikiverse_proxy.inc /etc/nginx/conf.d/wikiverse_proxy.inc
COPY --from=build /app/dist /usr/share/nginx/html

# Overridden by the platform. The defaults keep a local
# `docker build && docker run` working without extra flags.
ENV BACKEND_ORIGIN=https://backend-production-25f12.up.railway.app \
    BACKEND_HOST=backend-production-25f12.up.railway.app

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]