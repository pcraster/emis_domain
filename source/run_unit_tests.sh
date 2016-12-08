#!/usr/bin/env bash
set -e


docker build -t test/domain .
docker run --env ENV=TEST -p5000:5000 test/domain
