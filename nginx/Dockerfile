FROM nginx:latest

WORKDIR /etc/nginx

RUN apt install nginx-module-njs

RUN mkdir /var/log/nginx/payment-log && mkdir /var/log/nginx/bot-log

COPY nginx.conf router.js ./