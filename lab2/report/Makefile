all: clean report

report: report.pdf

report.pdf:
	mkdir -p aux
	latexmk -lualatex -shell-escape -auxdir=aux report.tex

clean:
	latexmk -C -auxdir=aux report.tex

.PHONY: all report clean
