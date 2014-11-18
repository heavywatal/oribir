MAIN := Oribir.py
SRCS := chromosome.py individual.py population.py simulation.py selection.py ${MAIN} qaction.py qchart.py qgraphics.py qparams.py translations/pyqt4.pro

.DEFAULT_GOAL := all
.PHONY: all clean open run methods exe app

all:
	$(MAKE) build

clean:
	$(RM) -rf *.pyc build/ dist/

open:
	open -a mi ${SRCS}

run: translations.py
	python ${MAIN}

translations.py: translations/ja_JP.ts ${SRCS}
	pylupdate4 -verbose translations/pyqt4.pro
	lrelease $<
	pyrcc4 translations.qrc -o translations.py

methods: methods.md
	pandoc $< -o build/methods.docx
