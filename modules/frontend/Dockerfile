# Step 1: Build the React app
FROM node:14.8.0-alpine3.12 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build

# Step 2: Serve the app with a lightweight HTTP server
FROM node:14.8.0-alpine3.12

# Install 'serve' globally
RUN npm install -g serve

WORKDIR /app

# Copy build artifacts from the builder stage
COPY --from=builder /app/build ./build

# Expose the port serve will run on
EXPOSE 3000

# Start the app
CMD ["serve", "-s", "build", "-l", "3000"]
