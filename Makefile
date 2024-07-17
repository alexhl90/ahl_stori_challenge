base:
	docker-compose -f ./infrastructure/compose.yml up --build --abort-on-container-exit

run-local:
	ARG1="offline" $(MAKE) base
deploy:
	ARG1="deploy" $(MAKE) base
info:
	ARG1="info" $(MAKE) base
remove:
	ARG1="remove" $(MAKE) base
	