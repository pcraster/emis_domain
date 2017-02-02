#!/usr/bin/env bash
set -e


docker build -t test/emis_domain .
docker run \
    --env ENV=DEVELOPMENT \
    -p5000:5000 \
    -v$(pwd)/emis_domain:/emis_domain \
    test/emis_domain
