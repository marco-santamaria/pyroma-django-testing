export DBNAME ?=blog

reset-db:
	# initializing database '${DBNAME}'
	@sh -c "psql -c 'DROP DATABASE IF EXISTS ${DBNAME};' -U postgres;"
	@sh -c "psql -c 'CREATE DATABASE ${DBNAME};' -U postgres;"

migrate-db:
	# migrating db
	./manage.py migrate

init-db: reset-db migrate-db
