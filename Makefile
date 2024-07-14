
run_dev:
	poetry run fastapi dev main.py

run_prod:
	poetry run fastapi run main.py
migrate:
	poetry run python run_migration.py