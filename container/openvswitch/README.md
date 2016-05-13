This is a very minimal openvswitch container.

It can be used as a daemon to sit on each host.
Other containers can then use openvswitch.
They just need to mount in /var/run/openvswitch

http://kubernetes.io/docs/admin/daemons/
