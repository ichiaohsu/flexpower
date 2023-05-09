FROM node:18.16-alpine AS builder

WORKDIR /app

COPY . .

RUN npm run build

ENV NODE_ENV=production

EXPOSE 3000

FROM nginx:latest

COPY --from=builder /app/build/ /usr/share/nginx/html

EXPOSE 80
