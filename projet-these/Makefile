LATEXMK ?= latexmk
BUILD := build
SOURCES := projet-these-fr.tex projet-these-en.tex
PDFS := $(SOURCES:%.tex=$(BUILD)/%.pdf)

.PHONY: all clean

all: $(PDFS)

$(BUILD)/%.pdf: %.tex ../bibliographie/references.bib
	@mkdir -p $(BUILD)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) $<

clean:
	@for source in $(SOURCES); do \
		$(LATEXMK) -C -output-directory=$(BUILD) $$source; \
	done
	@rm -rf $(BUILD)

