#!/bin/bash -ex
export CP_VERSION=$(cat VERSION)
exec supervisord -n -c supervisord.conf
