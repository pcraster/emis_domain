#!/usr/bin/env bash
set -e
docker build -t test/domain .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/domain:/domain test/domain
