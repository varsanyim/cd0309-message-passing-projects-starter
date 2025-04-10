# Build step
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npm install
COPY . ./
RUN npm run build

# Serve step
FROM node:20-alpine

WORKDIR /app
RUN npm install -g serve@13.0.2

COPY --from=builder /app/build ./build

EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
