Origami Bird Simulator for Education
====================================

Takahiro Yamanoi and Watal M. Iwasaki (2015)
Origami Bird Simulator: a teaching resource linking natural selection and speciation.
[*Evolution: Education and Outreach* **8** 1 (in press)](http://link.springer.com/journal/12052/8/1/)

Download an executable file
---------------------------

https://github.com/heavywatal/oribir/releases

Build from source code
----------------------

1. Install requirements:
   [Qt4](http://qt-project.org/),
   [PyQt4](http://www.riverbankcomputing.com/software/pyqt/intro),
   [numpy](http://www.numpy.org/), and [matplotlib](http://matplotlib.org/).

   ```
   % brew install qt
   % brew install pyqt
   % brew install numpy
   % brew install matplotlib --with-pyqt
   ```

   [Anaconda](http://continuum.io/) is an easy way for Windows.

1. Install [PyInstaller](http://www.pyinstaller.org/).

   ```
   % git clone https://github.com/pyinstaller/pyinstaller.git
   % python pyinstaller/setup.py install --user
   ```

   Windows needs [pywin32](http://sourceforge.net/projects/pywin32/files/pywin32/) too.

1. Put `.pth` file in the user `site-packages` directory.

   ```
   % echo "$(brew --prefix)/lib/python2.7/site-packages" > ~/Library/Python/2.7/lib/python2.7/site-packages/homebrew.pth
   ```

1. Download source.

   ```
   % git clone https://github.com/heavywatal/oribir.git
   % cd oribir/
   ```

1. Run.

   ```
   % make run
   ```

1. Build executable app.

   ```
   % /path/to/pyinstaller -yw Oribir.py
   ```

Web Application
---------------

[Web-app version](http://heavywatal.github.io/oribir.js/) will be available soon!
It is under development at https://github.com/heavywatal/oribir.js
