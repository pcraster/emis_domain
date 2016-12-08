#!/usr/bin/env bash
set -e


docker build -t test/domain .
docker run -p3031:3031 test/domain
