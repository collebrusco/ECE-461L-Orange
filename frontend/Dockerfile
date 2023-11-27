FROM node:18-alpine

ARG ENV
ENV REACT_APP_ENV $ENV

# Install dependencies
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm install

# Copy the rest and build
COPY . /app
RUN npm run build

EXPOSE 3000

CMD [ "npm", "run", "deploy" ]
