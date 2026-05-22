FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json ./
COPY apps/web/package.json ./apps/web/package.json
RUN npm install

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm --workspace apps/web run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/apps/web ./apps/web
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["npm", "--workspace", "apps/web", "run", "start"]
