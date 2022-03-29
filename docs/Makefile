.DEFAULT_GOAL := help
SPHINXOPTS    ?= -W
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = ./
BUILDDIR      = build

.PHONY: help
help:	## Show this help
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: Makefile
# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: test-local-docs
test-local-docs:
	docker run -it --rm -v `PWD`:/repo containers.cisco.com/aide/sphinx-tools validate.sh

.PHONY: show-local-docs
show-local-docs:
	rm -rf build || true
	docker run -it --rm -p 8000:8000 -w /repo -v `PWD`:/repo \
		-e SOURCEDIR=$(SOURCEDIR) \
		-e BUILDDIR=$(BUILDDIR) \
		containers.cisco.com/aide/sphinx-tools \
		cicd.sh
