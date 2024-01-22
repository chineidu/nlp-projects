.PHONY: help setup_venv run_test create_db drop_db


help:
	@echo "Commands:"
	@echo "\tsetup_venv:          create a virtual environment (REQUIRED)."
	@echo "\trun_test:            run the tests."
	@echo "\tcreate_db:           create the database."
	@echo "\tdrop_db:             drop the database."
	@echo

setup_venv:
	@echo
	@echo ">>>> Setting up virtual environment. <<<<"
	poetry lock "--no-update" && poetry install --no-interaction

run_test: setup_venv
	poetry run ${MAKE} __test__

__test__:
	@echo
	@echo ">>>> Running tests. <<<<"
	pytest -svvW ignore

create_db:
	poetry run ${MAKE} __create_db__

__create_db__:
	@echo
	@echo ">>>> Creating the DB. <<<<"
	python e_commerce_app/database.py --command 'create_db' database-manager

drop_db:
	poetry run ${MAKE} __drop_db__

__drop_db__:
	@echo
	@echo ">>>> Dropping the DB. <<<<"
	python e_commerce_app/database.py --command 'drop_db' database-manager
