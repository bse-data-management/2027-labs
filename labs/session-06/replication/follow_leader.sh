#!/bin/sh
# Copy the leader once it accepts connections, then start as its follower.
set -e

until pg_isready -q -h leader -U labs; do
    sleep 1
done

mkdir -p "$PGDATA"
chown postgres "$PGDATA"
chmod 700 "$PGDATA"
# -R writes the settings that make this server a follower of the leader.
PGPASSWORD=labs gosu postgres pg_basebackup -h leader -U labs -D "$PGDATA" -R -X stream

exec docker-entrypoint.sh postgres
