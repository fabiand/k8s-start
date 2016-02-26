

.PHONY: hl ll ngn

hl: host controller ll

ll: libvirt

ngn: ngn-builder

%: %/Dockerfile $(wildcard $*/*)
	docker build -f $< --tag fabiand/$*:latest $*
	docker push fabiand/$*:latest
