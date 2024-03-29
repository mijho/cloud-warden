SHELL		:= /bin/bash
version		:= 0.0.1
author		:= Mark Johnson
function 	:= To facilitate making lambda packages

.PHONY: env run help lint requirements
.DEFAULT: help

# List and check for commands.
COMMANDS = make
COMMAND_CHECK := $(foreach exec,$(COMMANDS), $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
BLUE   := $(shell tput -Txterm setaf 4)
RESET  := $(shell tput -Txterm sgr0)

TARGET_MAX_CHAR_NUM=60

help:
	@echo ''
	@echo '-----------------------------------------------------------------------------'
	@echo '${YELLOW}Author 	:	${GREEN}$(author)${RESET}'
	@echo '${YELLOW}Version :	${GREEN}$(version)${RESET}'
	@echo '${YELLOW}Function:	${GREEN}$(function)${RESET}'
	@echo '-----------------------------------------------------------------------------'
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo 'Add ${GREEN}TAG=X.X.X${RESET} to override latest tag'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

env:
	@echo "Building the python environment..."
	@python3 -m venv .venv
	@poetry install

lint:
	@echo "Running flake8"
	@poetry run flake8

run:
	@SAWMILL_DEVELOPER_LOGS=true aws-vault exec ${ACCOUNT} -- poetry run python cloud-warden/rounds.py

requirements:
	@poetry show --no-dev | tr -s " " | sed 's/ /==/' | sed 's/ .*//' > requirements.txt
	@gsed -i 's/sawmill.*/git+https:\/\/github.com\/mirrorweb\/sawmill@master/g' requirements.txt
