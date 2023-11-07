#!/bin/sh

. "$(dirname "$0")/db.sh"

sqlite3 $db < config/initial_data.sql
echo "Data loaded to $db"