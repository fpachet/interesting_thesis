LATEXMK ?= latexmk
SOURCE := projet-these.tex
BUILD := build

.PHONY: all clean

all:
	@mkdir -p $(BUILD)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -output-directory=$(BUILD) $(SOURCE)

clean:
	$(LATEXMK) -C -output-directory=$(BUILD) $(SOURCE)
	@rm -rf $(BUILD)

