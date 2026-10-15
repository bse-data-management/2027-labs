#!/bin/sh
# Runs once, when the leader is first created: let the follower connect to
# stream the leader's changes.
echo "host replication all all scram-sha-256" >> "$PGDATA/pg_hba.conf"
