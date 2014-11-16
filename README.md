Origami Bird Simulator for Education
====================================

Development
-----------

1. Install requirements:
   [Qt4](http://qt-project.org/),
   [PyQt4](http://www.riverbankcomputing.com/software/pyqt/intro),
   [numpy](http://www.numpy.org/), and [matplotlib](http://matplotlib.org/)

   ```
   % brew install qt
   % brew install pyqt
   % brew install numpy
   % brew install matplotlib --with-pyqt
   ```

1. Put `.pth` file in the user `site-packages` directory.

   ```
   % echo "$(brew --prefix)/lib/python2.7/site-packages" > ~/Library/Python/2.7/lib/python2.7/site-packages/homebrew.pth
   ```

1. Download source

   ```
   % git clone https://github.com/heavywatal/oribir.git ~/git/oribir
   % cd ~/git/oribir
   ```

1. Run

   ```
   % make run
   ```

1. Build executable app with [PyInstaller](http://www.pyinstaller.org/)
