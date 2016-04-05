FROM nginx:alpine

ENV CONTROLLER_PORT_8084_TCP_ADDR localhost
ENV CONTROLLER_PORT_8084_TCP_PORT 8084
ENV ENGINE_HOST localhost
ENV ENGINE_PORT 8443

COPY nginx.conf    /etc/nginx/nginx.conf
COPY k8s.json      /usr/share/ovirt-engine/ui-plugins/
COPY k8s/*         /usr/share/ovirt-engine/ui-plugins/k8s/
COPY nginx.crt     /etc/nginx/ssl/
COPY nginx.key    /etc/nginx/ssl/

COPY run.sh /

CMD /bin/sh /run.sh
