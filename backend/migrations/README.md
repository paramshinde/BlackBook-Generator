# Placeholder for Alembic migration scripts.
Run:
flask --app run db init
flask --app run db migrate -m "init"
flask --app run db upgrade
