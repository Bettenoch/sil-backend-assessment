#! /usr/bin/env bash

set -e
set -x

# Debugging permissions
echo "Checking permissions of the script:"
ls -l /app/scripts/prestart.sh

# Debugging ownership
echo "Checking ownership of the directory and script:"
ls -l /app/scripts

# Debugging environment variables
echo "Environment Variables:"
echo "POSTGRES_DB=$POSTGRES_DB"
echo "POSTGRES_USER=$POSTGRES_USER"
echo "POSTGRES_SERVER=$POSTGRES_SERVER"
echo "POSTGRES_PORT=$POSTGRES_PORT"

echo "Waiting for database connection..."
until python -c "import psycopg; psycopg.connect('dbname=$POSTGRES_DB user=$POSTGRES_USER password=$POSTGRES_PASSWORD host=$POSTGRES_SERVER port=$POSTGRES_PORT') and print('Connection successful')"; do
    echo "Database is unavailable - sleeping"
    sleep 3
done

echo "Database is available - continuing with script"

# Let the DB start
echo "Running backend_pre_start.py..."
python app/backend_pre_start.py

# Run migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Create initial data in DB
echo "Creating initial data..."
python app/initial_data.py

echo "Prestart script completed."
