

.PHONY: hl ll ngn

hl: compute controller ll

ll: libvirt

ngn: ngn-builder

%: %/Dockerfile $(wildcard $*/*)
	docker build -f $< --tag docker.io/fabiand/$*:latest $*
	docker push docker.io/fabiand/$*:latest
