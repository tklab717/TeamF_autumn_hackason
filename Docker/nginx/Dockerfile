FROM nginx

# nginxのローカルの設定ファイルをコンテナにコピー
COPY Docker/nginx/nginx.conf /etc/nginx/nginx.conf
# ADD Docker/nginx/conf.d/uwsgi.conf /etc/nginx/conf.d/uwsgi.conf

CMD ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]