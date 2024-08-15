FROM nginx
COPY ./nginx/ft_transcendence.conf.template /etc/nginx/conf.d/ft_transcendence.conf.template
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
