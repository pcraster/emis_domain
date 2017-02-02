#!/usr/bin/env bash
set -e


docker build -t test/emis_domain .
docker run -p3031:3031 test/emis_domain
