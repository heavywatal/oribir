SRCS := chromosome.py individual.py population.py simulation.py selection.py qaction.py qchart.py qgraphics.py qparams.py qtapp.py setup.py translations/pyqt4.pro

.DEFAULT_GOAL := all
.PHONY: all clean build open run

all:
	$(MAKE) build

clean:
	$(RM) -rf *.pyc log*log Oribir-darwin

open:
	tx ${SRCS}

run:
	python qtapp.py

build:
	python setup.py

tr:
	pylupdate4 -verbose translations/pyqt4.pro
	open translations/ja_JP.ts
	less translations/ja_JP.ts
	lrelease translations/ja_JP.ts
	pyrcc4 translations.qrc -o translations.py

