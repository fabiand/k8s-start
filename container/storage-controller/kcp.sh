#!/bin/bash -xe

function help()
{
	echo "Usage:"
	echo "ksp <pod name> <local file> <location in pod>"
}

if [ -z $1 ]
then
	help
	exit 1
fi

cat $2 | kubectl exec -ti $1 -- /bin/bash -c "cat > $3//$2"