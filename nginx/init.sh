
envsubst '${LOCALHOST}' < /etc/nginx/conf.d/ft_transcendence.conf.template > /etc/nginx/conf.d/ft_transcendence.conf

echo "Configuration Nginx mise à jour avec LOCALHOST=${LOCALHOST}"
