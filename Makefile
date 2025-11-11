HOME_PROJECT := $(shell pwd)
PYTHONPATH := $(PWD):$(PYTHONPATH)
PYTHON := PYTHONPATH=$(PWD):$(PYTHONPATH) $(HOME_PROJECT)/.env/bin/python3

help:
	@echo help


exec:
	@if [ -z "$(strip $(args))" ]; then \
		$(PYTHON) $(file); \
	else \
		$(PYTHON) $(file) $(args); \
	fi
