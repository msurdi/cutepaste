.PHONY: default deps base build start stop shell run test push

# Name of this service/application
SERVICE_NAME := cutepaste

# Shell history file
HISTORY_FILE := ~/.bash_history.$(SERVICE_NAME)

# Get the current version of the project
export VERSION ?= $(shell git rev-parse --short HEAD)

# Get current branch name
export BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

# Shell to use for running scripts
SHELL := $(shell which bash)

# Get docker path or an empty string
DOCKER := $(shell command -v docker)

# Bash history file for container shell
HISTORY_FILE := ~/.bash_history.$(SERVICE_NAME)

# Build environment (must exist a directory with a docker-compose.yml file in build/$BUILD_ENV)
BUILD_ENV ?= dev

# Docker compose command
COMPOSE := $(DOCKER) run --env-file <(env) -it --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$(PWD)":"$(PWD)" --workdir="$(PWD)" dduportal/docker-compose:latest

COMPOSE_ENV := $(COMPOSE) -f build/$(BUILD_ENV)/docker-compose.yml

COMPOSE_ENV_CMD := $(COMPOSE_ENV) run --rm $(SERVICE_NAME)

# The default action of this Makefile is to build the development docker image
default: build
# Test if the dependencies we need to run this Makefile are installed
deps:
ifndef DOCKER
	@echo "Docker is not available. Please install docker"
	@exit 1
endif
	mkdir -p .data/{cutepaste} node_modules

base: deps
	$(COMPOSE) -f build/base/docker-compose.yml build

build: base
	$(COMPOSE_ENV) build

start: build
	$(COMPOSE_ENV) up --force-recreate

stop:
	$(COMPOSE_ENV) stop
	$(COMPOSE_ENV) rm -f -v

run: build
	$(COMPOSE_ENV) run --rm --service-ports $(SERVICE_NAME)

shell: build
	-touch $(HISTORY_FILE)
	$(COMPOSE_ENV_CMD) /bin/bash

test: build
	$(COMPOSE_ENV_CMD) pytest --runslow

push:
	BUILD_ENV=prod make
	$(DOCKER) tag msurdi/cutepaste:latest msurdi/cutepaste:$(BRANCH)
	$(DOCKER) push msurdi/cutepaste:$(BRANCH)
