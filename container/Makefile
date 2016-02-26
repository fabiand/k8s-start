

push: build
	docker push fabiand/libvirtd:latest
	docker push fabiand/libvirt-client:latest

build: libvirtd libvirt-client

libvirtd: Dockerfile.server
	docker build -f $< --tag fabiand/libvirtd:latest .

libvirt-client: Dockerfile.client start-controller.sh
	docker build -f $< --tag fabiand/libvirt-client:latest .

node-next-builder: N=fabiand/node-next-builder:latest
node-next-builder: Dockerfile.ngn-builder
	docker build -f $< --tag $(N) .
	docker push $(N)
