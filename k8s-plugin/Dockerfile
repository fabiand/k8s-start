FROM nginx:alpine

ENV CONTROLLER_HOST localhost
ENV CONTROLLER_PORT 8080
ENV ENGINE_HOST localhost
ENV ENGINE_PORT 8080

COPY nginx.conf    /etc/nginx/nginx.conf
COPY k8s.json      /usr/share/ovirt-engine/ui-plugins/
COPY k8s/*         /usr/share/ovirt-engine/ui-plugins/k8s/

COPY run.sh /

CMD /bin/sh /run.sh
