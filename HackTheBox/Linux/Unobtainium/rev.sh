#!/bin/bash

RHOST="127.0.0.1"
RPORT=3000
UA="Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
PROXY="127.0.0.1:8080"
FILE=$1

cat - <<EOF > message.json
{
    "auth":
    {
        "name":"felamos",
        "password":"Winter2021"
    },
    "filename":"${FILE}"
}
EOF

curl -s \
     -A "${UA}" \
     -H "Content-Type: application/json" \
     -d "$(cat message.json | jq -c)" \
     -x "${PROXY}" \
     -o /dev/null \
     "http://${RHOST}:${RPORT}/upload"