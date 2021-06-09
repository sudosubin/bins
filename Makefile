.EXPORT_ALL_VARIABLES:
root := $(patsubst %/,%,$(dir $(realpath $(lastword $(MAKEFILE_LIST)))))
PYTHONWARNINGS := ignore:Unverified HTTPS request
unexport root

ifneq (,$(wildcard $(root)/.makerc))
	include $(root)/.makerc
endif

define message
	echo "$$(tput setaf 2)$(strip $(1))$$(tput sgr 0)"
endef

.PHONY: bootstrap
bootstrap: install check run

.PHONY: install
install:
	@if [ ! -d "$(root)/.venv" ]; then \
		$(call message, Create Virtualenv); \
		/usr/bin/python3 -m venv "$(root)/.venv"; \
		printf "Done\n\n"; \
	fi

	@$(call message, Install python packages)
	@"$(root)/.venv/bin/pip" install -U -r "$(root)/requirements.txt"
	@echo ""

.PHONY: check
check:

.PHONY: run
play:
