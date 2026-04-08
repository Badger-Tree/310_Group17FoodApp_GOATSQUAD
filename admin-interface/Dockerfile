# Admin Interface Dockerfile
# Use Node.js for building and serving the admin app
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
ENV NODE_ENV=development
RUN npm install
COPY . .
RUN npx vite build
# Use a simple static server for production
RUN npm install -g serve
EXPOSE 3001
CMD ["serve", "-s", "dist", "-l", "3001"]
