# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
# No-warnings policy: any Sphinx warning fails the build; --keep-going
# reports all of them in one run instead of stopping at the first.
SPHINXOPTS    = -W --keep-going
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# CI-equivalent build: wipe all git-ignored files under docs/ before
# building (see the "Fresh-state verification" policy in docs/developer.rst).
fresh:
	git clean -fdX .
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile fresh

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
