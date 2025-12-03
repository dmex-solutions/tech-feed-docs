## $ docker image build -t qqs-tech-feed-docs -f Dockerfile .
## $ docker run --name tech-feed-docs -d --network br0 --ip 192.168.5.7 -p 9080:9080 qqs-tech-feed-docs:latest
## $ curl http://localhost:9080/health

# docker image build -t qqs-tech-feed-docs -f Dockerfile .
# docker tag qqs-tech-feed-docs:latest ramalin/tech-feed-docs:v25.10.1
# docker push ramalin/tech-feed-docs:v25.10.1


#################################
#  BUILD STAGE
#################################
FROM node:20-alpine AS build

WORKDIR /usr/src/app

# Copy dependency files
COPY package*.json ./
COPY package-lock.json ./
COPY .npmrc ./

# Install dependencies
RUN npm install

# Copy full project code (current directory context)
COPY . ./

# Run Docusaurus build
RUN npm run build


#################################
#  PRODUCTION STAGE
#################################
FROM node:20-alpine AS production

WORKDIR /usr/src/app

# Copy build output + modules from build stage
COPY --from=build /usr/src/app/node_modules ./node_modules
COPY --from=build /usr/src/app/build ./build

# Install serve globally (only in final stage)
RUN npm install -g serve

# Expose correct port
EXPOSE 8000

# Run as safe non-root user
USER node

# Start the site
CMD ["serve", "build", "-l", "8000"]
