# Docker Image which is used as foundation to create
# a custom Docker Image with this Dockerfile
FROM node:12.14.1-alpine as build-deps
# A directory within the virtualized Docker environment
# Becomes more relevant when using Docker Compose later
WORKDIR /usr/src/app
# Copies package.json and package-lock.json to Docker environment
COPY package*.json ./
RUN npm install

# Copies everything over to Docker environment
COPY . .

RUN npm build

FROM nginx:1.12-alpine
COPY --from=build-deps /usr/src/app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]