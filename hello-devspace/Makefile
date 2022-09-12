set_registry:
	@read -p "Enter your registry host: " REGISTRY && \
	yq e -i '.spec.template.spec.containers[0].image = "'$${REGISTRY}'/python-hello-devspace"' manifests/deployment.yaml && \
	yq e -i '.vars.REGISTRY = "'$${REGISTRY}'"' devspace.yaml