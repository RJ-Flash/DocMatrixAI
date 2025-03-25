# Minimal makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean livehtml linkcheck

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR)/*

livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

linkcheck:
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS) $(O)

# Custom targets for different output formats
pdf:
	@$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)/latex" $(SPHINXOPTS) $(O)
	@echo "Running LaTeX files through pdflatex..."
	@make -C "$(BUILDDIR)/latex" all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

epub:
	@$(SPHINXBUILD) -b epub "$(SOURCEDIR)" "$(BUILDDIR)/epub" $(SPHINXOPTS) $(O)
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

singlehtml:
	@$(SPHINXBUILD) -b singlehtml "$(SOURCEDIR)" "$(BUILDDIR)/singlehtml" $(SPHINXOPTS) $(O)
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

text:
	@$(SPHINXBUILD) -b text "$(SOURCEDIR)" "$(BUILDDIR)/text" $(SPHINXOPTS) $(O)
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

man:
	@$(SPHINXBUILD) -b man "$(SOURCEDIR)" "$(BUILDDIR)/man" $(SPHINXOPTS) $(O)
	@echo "Build finished. The manual pages are in $(BUILDDIR)/man."

changes:
	@$(SPHINXBUILD) -b changes "$(SOURCEDIR)" "$(BUILDDIR)/changes" $(SPHINXOPTS) $(O)
	@echo "The overview file is in $(BUILDDIR)/changes."

doctest:
	@$(SPHINXBUILD) -b doctest "$(SOURCEDIR)" "$(BUILDDIR)/doctest" $(SPHINXOPTS) $(O)
	@echo "Testing of doctests in the sources finished, look at the results in $(BUILDDIR)/doctest/output.txt."

coverage:
	@$(SPHINXBUILD) -b coverage "$(SOURCEDIR)" "$(BUILDDIR)/coverage" $(SPHINXOPTS) $(O)
	@echo "Testing of coverage in the sources finished, look at the results in $(BUILDDIR)/coverage/python.txt."

xml:
	@$(SPHINXBUILD) -b xml "$(SOURCEDIR)" "$(BUILDDIR)/xml" $(SPHINXOPTS) $(O)
	@echo "Build finished. The XML files are in $(BUILDDIR)/xml."

pseudoxml:
	@$(SPHINXBUILD) -b pseudoxml "$(SOURCEDIR)" "$(BUILDDIR)/pseudoxml" $(SPHINXOPTS) $(O)
	@echo "Build finished. The pseudo-XML files are in $(BUILDDIR)/pseudoxml."

# Development helpers
dev: clean livehtml

# Production build with all checks
prod: clean linkcheck html pdf epub 