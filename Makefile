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

process-txn:
	docker exec -it ahl_stori_challenge sh -c "npx serverless invoke local --function ProcessSummary"

generate-txn:
	docker exec -it ahl_stori_challenge sh -c "npx serverless invoke local --function GenerateHistory --data '{\"user_email\":\"$(EMAIL)\"}'"
