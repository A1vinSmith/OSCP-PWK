#!/bin/bash

RHOST="127.0.0.1"
RPORT=3000
UA="Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
PROXY="127.0.0.1:8080"
TEXT="$1"

cat - <<EOF > message.json
{
    "auth":
    {
        "name":"felamos",
        "password":"Winter2021"
    },
    "message":
    {
        "text":${TEXT}
    }
}
EOF

curl -s \
     -X PUT \
     -A "${UA}" \
     -H "Content-Type: application/json" \
     -d "$(cat message.json | jq -c)" \
     -x "${PROXY}" \
     "http://${RHOST}:${RPORT}/" \
| jq .