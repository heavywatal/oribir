Origami Bird Simulator for Education
====================================

Development
-----------

1. Install [Qt4](http://qt-project.org/) and
   [PyQt4](http://www.riverbankcomputing.com/software/pyqt/intro)
   ```
   % brew install qt
   % brew install pyqt
   ```

1. Create virtualenv for the project
   ```
   % easy_install --user pip
   % ~/Library/Python/2.7/bin/pip install --user virtualenv
   % cd ${ORIBIR}/
   % ~/Library/Python/2.7/bin/virtualenv virtualenv
   % source virtualenv/bin/activate
   % pip install numpy scipy matplotlib
   % echo "$(brew --prefix)/lib/python2.7/site-packages" > virtualenv/lib/python2.7/site-packages/homebrew.pth
   ```
1. Run
   ```
   % python qtapp.py
   ```

1. Build executable app with [PyInstaller](http://www.pyinstaller.org/)
