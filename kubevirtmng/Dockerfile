FROM fedora:23
MAINTAINER "Tolik Litovsky" <tlitovsk@redhat.com>
ENV container docker

RUN dnf -y install python
RUN dnf -y update && dnf clean all;

COPY ui /ui
ADD start.sh /

EXPOSE 8000

CMD /start.sh
# docker build --rm -t tlitovsk/kubevirt-ui:latest