HOME_PROJECT := $(shell pwd)
PYTHONPATH := $(PWD):$(PYTHONPATH)
PYTHON := PYTHONPATH=$(PWD):$(PYTHONPATH) /home/malick/miniconda3/envs/lazynotion/bin/python

help:
	@echo help


exec:
	@if [ -z "$(strip $(args))" ]; then \
		$(PYTHON) $(file); \
	else \
		$(PYTHON) $(file) $(args); \
	fi
