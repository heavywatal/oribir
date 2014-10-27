#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""
import sys
import os
import re
import shutil

import subprocess


def mod_spec(outdir, appname):
    spec_end = '''\
import sys
if sys.platform.startswith("darwin"):
    app = BUNDLE(exe,
                 appname=os.path.join("{outdir}", "{appname}.app"),
                 version=1.0)
'''.format(**locals())

    spec = os.path.join(outdir, appname) + ".spec"
    with open(spec, 'a+b') as fapp:
        print(spec_end)
        fapp.write(spec_end)
    return spec


def mod_plist(product):
    plist = os.path.join(product, "Contents", "Info.plist")
    with open(plist, 'r+') as fio:
        info = re.sub("<string>1</string>", "<false/>", fio.read())
        print(info)
        fio.seek(0)
        fio.write(info)
        fio.truncate()


def post_build(outdir, appname):
    product = os.path.join(outdir, appname + ".app")
    macos = os.path.join(product, "Contents", "MacOs")
    resources = os.path.join(product, "Contents", "Resources")
    #qt_menu_nib = "/opt/local/lib/Resources/qt_menu.nib"
    qt_menu_nib = "/Library/Frameworks/QtGui.framework/\
Versions/Current/Resources/qt_menu.nib"
    #mod_plist(product)

    subprocess.check_call(["rm", "-rf", macos])
    shutil.copytree(os.path.join(outdir, "dist", appname), macos)

    shutil.copytree(qt_menu_nib, os.path.join(resources, "qt_menu.nib"))


def makespec(src, appname=None, outdir=None):
    cmd = ["Makespec.py"]
    if sys.platform.startswith("darwin"):
        cmd.append("--onedir")
        cmd.append("--windowed")
    elif sys.platform.startswith("win"):
        cmd.append("--onefile")
        cmd.append("--windowed")
    else:
        cmd.append("--onefile")

    if appname:
        cmd.extend(["-n", appname])
    if outdir:
        cmd.extend(["-o", outdir])

    cmd.append(src)
    print(' '.join(cmd))
    output = subprocess.check_output(cmd)
    print(output.rstrip())
    return re.search("wrote (\S+)", output).group(1)


def build(spec):
    cmd = ["Build.py", spec]
    cmd.append("--noconfirm")
    print(' '.join(cmd))
    return subprocess.check_call(cmd)


def exists_on_path(command):
    PATH = os.getenv("PATH").split(':')
    return any([os.path.exists(os.path.join(d, command)) for d in PATH])


def search_alt_path(dirnames):
    for dir_ in dirnames:
        path_ = os.path.join(dir_, "pyinstaller.py")
        if os.path.exists(path_):
            return path_
    return "pyinstaller.py"


def pyinstaller(src, appname=None, outdir=None):
    cmd = []
    if exists_on_path("pyinstaller.py"):
        cmd.append("pyinstaller.py")
    else:
        path_cands = []
        path_cands.append(os.path.join(".", "pyinstaller"))
        path_cands.append(os.path.join("..", "pyinstaller"))
        home = os.path.expanduser("~")
        path_cands.append(os.path.join(home, "pyinstaller"))
        path_cands.append(os.path.join(home, "build", "pyinstaller"))
        pyinstaller_path = search_alt_path(path_cands)
        cmd.append(sys.executable)
        cmd.append(pyinstaller_path)
        #cmd.append(os.path.join(pyinstaller_path, "pyinstaller.py"))

    if sys.platform.startswith("darwin"):
        cmd.append("--onedir")
        cmd.append("--windowed")
    elif sys.platform.startswith("win"):
        cmd.append("--onefile")
        cmd.append("--windowed")
        #cmd.append("--noupx")
    else:
        cmd.append("--onefile")

    if appname:
        cmd.extend(["-n", appname])
    if outdir:
        cmd.extend(["-o", outdir])

    cmd.append("--noconfirm")
    cmd.append(src)
    return subprocess.check_call(cmd)


if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser(version="%prog 1.0")
    parser.set_usage("usage: %prog [options] [...]")

    parser.add_option("-v", "--verbose", action='store_true', default=False)
    parser.add_option("-n", "--appname", default="Oribir")
    parser.add_option("-o", "--outdir")

    (options, args) = parser.parse_args()
    print(args)

    if args:
        src = args[0]
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(here, "qtapp.py")

    appname = options.appname or os.path.basename(src).split(".")[0].title()
    outdir = options.outdir or '-'.join([appname, sys.platform])

    if False and sys.platform.startswith("darwin"):
        spec = makespec(src, appname, outdir)
#        outdir = os.path.dirname(spec)
#        appname = os.path.splitext(os.path.basename(spec))[0]
#        print(outdir, appname)
#        spec = mod_spec(outdir, appname)
        build(spec)
#        post_build(outdir, appname)

    else:
        pyinstaller(src, appname, outdir)
        sys.exit()

#if sys.platform == "linux2":
#    pass
#
#elif sys.platform == "darwin":
#    pass
#
#elif sys.platform = "win32":
#
#    from distutils.core import setup
#    import py2exe
#    import matplotlib
#
#    py2exe_options = {
#      "compressed": 1,
#      "optimize": 2,
#      "bundle_files": 3
#    }
#
#    setup(
#      windows=["gui.py"],
#      options={"py2exe": py2exe_options},
#      data_files=matplotlib.get_py2exe_datafiles()
#    )
