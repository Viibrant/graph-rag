# frontend/Dockerfile
FROM oven/bun:1 AS base
WORKDIR /app

# Cache deps
COPY frontend/package.json frontend/bun.lock ./
RUN bun install

# Dev stage
FROM base AS dev
WORKDIR /app
COPY frontend/ /app/
CMD ["bun", "run", "dev"]

# Build stage
FROM base AS build
WORKDIR /app
COPY frontend/ /app/
RUN bun run build

# Production stage (serve static files via nginx)
FROM nginx:alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
COPY frontend/nginx.default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]