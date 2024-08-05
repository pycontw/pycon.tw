.PHONY: init

init:
	. ${NVM_DIR}/nvm.sh && nvm use
	yarn install --dev
	poetry env use 3.10
	poetry install

run_db:
	docker compose -f docker-compose-dev.yml up db -d

run_local: init run_db
	export DATABASE_URL=postgresql://postgres:secretpostgres@127.0.0.1:5432/pycontw2016
	poetry run python src/manage.py runserver 0.0.0.0:8000

run_dev:
	docker compose -f docker-compose-dev.yml up -d --build
	docker compose -f docker-compose-dev.yml logs -f pycontw

stop_dev:
	docker compose -f docker-compose-dev.yml stop

remove_dev:
	docker compose -f docker-compose-dev.yml down

shell_dev:
	docker compose -f docker-compose-dev.yml exec -it pycontw /bin/sh
