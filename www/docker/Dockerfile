# ------------- Build stage --------------------
FROM node:23-alpine3.20 AS builder

ARG VITE_GIT_RANK_API_URL
ENV VITE_GIT_RANK_API_URL=$VITE_GIT_RANK_API_URL

COPY . /build
WORKDIR /build

RUN npm install && \
    npm run build

# ------------- Runtime stage --------------------
FROM nginx:1.28.0-alpine AS runtime

COPY --from=builder /build/dist /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf