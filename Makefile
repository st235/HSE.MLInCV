#
# This Makefile provides the following targets:
#   install:
#     activates virtual environment, installs all dependencies,
#     including dependencies for development, activates pre-commit
#     hooks
#   build:
#     provides pre-build binaries, includes wheels
#   test:
#     calls tests using pytest
#   format:
#     calls black to format codestyle
#   lint:
#     calls pylint to check the codebase
#   clean:
#     removes virtual environment, cleans Python cache
#   demo:
#     runs the library in demo mode
#

WORKDIR=.
VENVDIR=$(WORKDIR)/.venv

# Search Python command

ifndef PY
_PY_OPTION:=python3
ifeq (ok,$(shell $(_PY_OPTION) -c "print('ok')" $(NULL_STDERR)))
PY=$(_PY_OPTION)
endif
endif

ifndef PY
_PY_OPTION:=$(VENVDIR)/bin/python
ifeq (ok,$(shell $(_PY_OPTION) -c "print('ok')" $(NULL_STDERR)))
PY=$(_PY_OPTION)
$(info $(_PY_AUTODETECT_MSG))
endif
endif

ifndef PY
_PY_OPTION:=$(subst /,\,$(VENVDIR)/Scripts/python)
ifeq (ok,$(shell $(_PY_OPTION) -c "print('ok')" $(NULL_STDERR)))
PY=$(_PY_OPTION)
$(info $(_PY_AUTODETECT_MSG))
endif
endif

ifndef PY
_PY_OPTION:=py -3
ifeq (ok,$(shell $(_PY_OPTION) -c "print('ok')" $(NULL_STDERR)))
PY=$(_PY_OPTION)
$(info $(_PY_AUTODETECT_MSG))
endif
endif

ifndef PY
_PY_OPTION:=python
ifeq (ok,$(shell $(_PY_OPTION) -c "print('ok')" $(NULL_STDERR)))
PY=$(_PY_OPTION)
$(info $(_PY_AUTODETECT_MSG))
endif
endif

ifndef PY
define _PY_AUTODETECT_ERR
Could not detect Python interpreter automatically.
Please specify path to interpreter via PY environment variable.
endef
$(error $(_PY_AUTODETECT_ERR))
endif


VENV=$(VENVDIR)/bin
# Detect windows
ifeq (win32,$(shell $(PY) -c "import __future__, sys; print(sys.platform)"))
VENV=$(VENVDIR)/Scripts
endif

.PHONY: install build format lint clean test

install: requirements.txt dev-requirements.txt
	$(PY) -m pip install --user virtualenv
	$(PY) -m venv $(VENVDIR)
	. $(VENV)/activate
	$(PY) -m pip install --user --upgrade pip
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install -r dev-requirements.txt
	pre-commit install

build:
	. $(VENV)/activate
	$(PY) -m pip install --user --upgrade build
	$(PY) -m build

test:
	. $(VENV)/activate
	pytest .

lint:
	. $(VENV)/activate
	pylint .

format:
	. $(VENV)/activate
	black .

clean:
	rm -rf $(VENVDIR)
	find $(WORKDIR) -name "*.pyc" -delete

demo:
	. $(VENV)/activate
	python demo.py
