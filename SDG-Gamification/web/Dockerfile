FROM node:18-alpine

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

# Set environment variables for React dev server
ENV CI=false
ENV REACT_APP_API_URL=http://backend:8000/api/v1
ENV WDS_SOCKET_HOST=localhost
ENV WDS_SOCKET_PORT=3000

EXPOSE 3000

CMD ["npm", "start"]
