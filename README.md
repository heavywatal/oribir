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
   % ~/Library/Python/2.7/bin/virtualenv ~/.virtualenv/oribir
   % source ~/.virtualenv/oribir/bin/activate
   (oribir)% echo "$(brew --prefix)/lib/python2.7/site-packages" > ${VIRTUAL_ENV}/lib/python2.7/site-packages/homebrew.pth
   ```

1. Install [numpy](http://www.numpy.org/),
   [scipy](http://www.scipy.org/), [matplotlib](http://matplotlib.org/)
   ```
   (oribir)% pip install numpy matplotlib
   ```

1. Download source
   ```
   (oribir)% git clone https://github.com/heavywatal/oribir.git ~/git/oribir
   (oribir)% cd ~/git/oribir
   ```

1. Run
   ```
   (oribir)% make run
   ```

1. Build executable app with [PyInstaller](http://www.pyinstaller.org/)
