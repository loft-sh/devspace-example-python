#!/bin/bash
set +e  # Continue on errors

echo "api devspace-example-python-simple.${NAMESPACE}.svc.cluster.local" > /etc/host.aliases
echo "export HOSTALIASES=/etc/host.aliases" >> /etc/profile
. /etc/profile

bash