#!/bin/bash -ex
export CP_VERSION=$(cat VERSION)
exec uwsgi --ini uwsgi.ini
