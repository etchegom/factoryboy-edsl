#!make

confirm-erase:
	@echo "This operation will erase stored data. Proceed? (yN) " && read ans && [ $${ans:-N} = y ]

stop: confirm-erase
	@docker-compose down -v

start:
	@docker-compose up -d --build

pre-commit:
	@pre-commit run --all-files
