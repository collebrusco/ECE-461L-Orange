FROM node:18-alpine

ENV REACT_APP_ENV development

WORKDIR /frontend
COPY . .

# Install dependencies and build
RUN npm install
RUN npm run build

EXPOSE 3000

CMD [ "npm", "run", "deploy" ]
