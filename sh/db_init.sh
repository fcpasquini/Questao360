#!/bin/sh

. "$(dirname "$0")/db.sh"

mkdir -p "data/db"

if test -f $db; then
    echo "$db exists. Exiting."
    exit 1
fi

sqlite3 $db < config/db_schema.sql
echo "Created $db"