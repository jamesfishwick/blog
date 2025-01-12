#!/bin/bash

# Step 1: Check for Docker installation
echo -e "Checking for Docker installation...\n"
if ! command -v docker > /dev/null 2>&1; then
    echo -e "Docker is not installed. Please install Docker and try again.\n"
    exit 1
fi

# Step 2: Start PostgreSQL container
echo -e "Starting PostgreSQL container...\n"
CONTAINER_NAME="postgres-dev"
DB_NAME="test_db"
POSTGRES_PASSWORD="password"

if [ "$(docker ps -aq -f name="$CONTAINER_NAME")" ]; then
    echo -e "Container $CONTAINER_NAME already exists. Starting it...\n"
    docker start "$CONTAINER_NAME"else
    echo -e "Creating and starting a new PostgreSQL container named $CONTAINER_NAME...\n"
    docker run --name $CONTAINER_NAME -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD -d -p 5432:5432 postgres
    echo -e "Container $CONTAINER_NAME created successfully.\n"
fi

# Wait for PostgreSQL to be ready
echo -e "Waiting for PostgreSQL to be ready...\n"
for i in {1..10}; do
    if docker exec $CONTAINER_NAME pg_isready -U postgres > /dev/null 2>&1; then
        echo -e "PostgreSQL is ready.\n"
        break
    fi
    echo -e "PostgreSQL is not ready yet. Retrying in 2 seconds...\n"
    sleep 2
done

# Step 3: Check if the database exists
echo -e "Checking if database $DB_NAME exists...\n"
if docker exec $CONTAINER_NAME psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME';" | grep -q 1; then
    echo -e "Database $DB_NAME already exists. Skipping creation.\n"
else
    echo -e "Creating database: $DB_NAME\n"
    if docker exec $CONTAINER_NAME psql -U postgres -c "CREATE DATABASE $DB_NAME;"; then
        echo -e "Database $DB_NAME created successfully.\n"
    else
        echo -e "Failed to create database $DB_NAME. Check logs for details.\n"
        docker logs $CONTAINER_NAME
        exit 1
    fi
fi

# Step 4: Export environment variable
echo -e "Exporting DATABASE_URL...\n"
export DATABASE_URL="postgres://postgres:$POSTGRES_PASSWORD@localhost/$DB_NAME"
echo -e "DATABASE_URL set to: $DATABASE_URL\n"

# Final Check: Quick Exit if Setup is Already Complete
echo -e "Database setup complete. Everything is up-to-date.\n"
