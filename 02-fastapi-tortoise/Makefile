set_registry:
	@read -p "Enter your registry host: " REGISTRY && \
	yq e -i '.spec.template.spec.containers[0].image = "'$${REGISTRY}'/python-simple-project-backend"' manifests/deployment.yaml && \
	yq e -i '.spec.template.spec.containers[1].image = "'$${REGISTRY}'/python-simple-project-db"' manifests/deployment.yaml && \
	yq e -i '.vars.REGISTRY = "'$${REGISTRY}'"' devspace.yaml