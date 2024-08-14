FROM node:latest

EXPOSE 3000

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

COPY .env .env

COPY init.sh /init.sh

RUN chmod +x /init.sh
RUN /init.sh

CMD ["npm", "run", "dev"]
