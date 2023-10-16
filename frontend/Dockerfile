FROM node:18-alpine

WORKDIR /frontend
COPY . .

# Install dependencies and build
RUN npm install
RUN npm run build

# Remove everything but build/
# RUN rm -rf README.md package*.json .gitignore src public node_modules

EXPOSE 3000

CMD ["npm", "run", "start"]
