#!/usr/bin/env sh

curl -i -H "Accept: application/json" -X POST -d @event.json http://localhost:10000

