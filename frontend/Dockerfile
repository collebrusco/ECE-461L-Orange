FROM node:18-alpine

ARG ENV
ENV REACT_APP_ENV $ENV

WORKDIR /frontend
COPY . .

# Install dependencies and build
RUN npm install
RUN npm run build

EXPOSE 3000

CMD [ "npm", "run", "deploy" ]
