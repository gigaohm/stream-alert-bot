VENV_NAME?=venv
VENV_BIN=$(shell pwd)/${VENV_NAME}/bin
PYTHON=${VENV_BIN}/python3

help:
	@echo "  build     Builds with Nix"
	@echo "  shell     Creates a nix-shell"
	@echo "  clean     Removes unwanted stuff"
	@echo "  lint      Check style with pycodestyle"
	@echo "  venv      Creates virtual environment"

build:
	nix-build nix/release.nix

shell:
	nix-shell nix

clean:
	rm -rf build
	rm -rf dist
	rm -rf venv
	rm -rf result
	rm -rf twitch_alert_bot.egg-info
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

lint:
	nix-shell nix --pure --run "pycodestyle tab"

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip setuptools
	${PYTHON} -m pip install -e .[devel]
	touch $(VENV_NAME)/bin/activate
