SRCS := chromosome.py individual.py population.py simulation.py selection.py qaction.py qchart.py qgraphics.py qparams.py qtapp.py setup.py translations/pyqt4.pro

.DEFAULT_GOAL := all
.PHONY: all clean open run build

all:
	$(MAKE) build

clean:
	$(RM) -rf *.pyc build/ dist/

open:
	open -a mi ${SRCS}

run: translations.py
	python qtapp.py

build:
	pyinstaller --windowed -n OBS -y -d qtapp.py
#	python setup.py

translations.py: ${SRCS}
	pylupdate4 -verbose translations/pyqt4.pro
	lrelease translations/ja_JP.ts
	pyrcc4 translations.qrc -o translations.py

methods: methods.md
	pandoc $< -o build/methods.docx
