.EXPORT_ALL_VARIABLES:
root := $(patsubst %/,%,$(dir $(realpath $(lastword $(MAKEFILE_LIST)))))
PYTHONWARNINGS := ignore:Unverified HTTPS request
unexport root

ifneq (,$(wildcard $(root)/.makerc))
	include $(root)/.makerc
endif

.PHONY: bootstrap
bootstrap: prepare check install

.PHONY: prepare
prepare:
	@if [ ! -d "$(root)/.venv" ]; then \
		echo "$$(tput setaf 6)Creating virtualenv$$(tput sgr 0) in $(root)/.venv"; \
		/usr/bin/python3 -m venv "$(root)/.venv"; \
	fi

	@echo "$$(tput setaf 6)Installing dependencies$$(tput sgr 0) in $(root)/.venv"
	@"$(root)/.venv/bin/pip" install -U -q wheel
	@"$(root)/.venv/bin/pip" install -U -q -r "$(root)/requirements.txt"

.PHONY: check
check:
	@"$(root)/.venv/bin/python" "$(root)/src/main.py" check

.PHONY: install
install:
	@"$(root)/.venv/bin/python" "$(root)/src/main.py" install
