import os
import argparse
import re
import shutil
import stat
import urllib.request
import platform
import tarfile
import subprocess
from zipfile import ZipFile as zipfile
from pathlib import Path as path

# From https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
# For compatibility with Python < 3.8
def copytree(src, dst, symlinks = False, ignore = None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
            if os.path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except:
                pass # lchmod not available
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def execute_replace(input, script):
   i = 0
   script_len = len(script)
   while True:
      while i < script_len:
         if script[i] == '/\n':
            i += 1
            break
         i += 1
      if i >= script_len:
         break
      before = ''
      while i < script_len:
         if script[i] == '/\n':
            i += 1
            break
         before += script[i]
         i += 1
      if i >= script_len:
         break
      after = ''
      while i < script_len:
         if script[i] == '/\n':
            i += 1
            break
         after += script[i]
         i += 1
      input = input.replace(before, after)
      if i >= script_len:
         break
   return input

def replacego(filepath):
    filepathname = os.path.join(filepath, "pdftron_wrap.cxx")
    with open(filepathname, "r") as f:
       cxx = f.read()

    filepathname = os.path.join(filepath, "pdftron_wrap.h")
    with open(filepathname, "r") as f:
       h = f.read()

    filepathname = os.path.join(filepath, "pdftron.go")
    with open(filepathname, "r") as f:
       go = f.read()

    filepathname = os.path.join(filepath, "pdftron_wrap.cxx.replace")
    with open(filepathname, "r") as f:
       cxx_replace = f.readlines()

    filepathname = os.path.join(filepath, "pdftron_wrap.h.replace")
    with open(filepathname, "r") as f:
       h_replace = f.readlines()

    filepathname = os.path.join(filepath, "pdftron.go.replace")
    with open(filepathname, "r") as f:
       go_replace = f.readlines()

    uid = re.search(r'(extern\s+\w+\s+_wrap_\w+_pdftron_)(\w+)(\()', go).group(2)

    go = execute_replace(go, go_replace)
    cxx = execute_replace(cxx, cxx_replace)
    h = execute_replace(h, h_replace)

    old_uid = '02581caacfa652f4'
    go = go.replace(old_uid, uid)
    cxx = cxx.replace(old_uid, uid)
    h = h.replace(old_uid, uid)

    filepathname = os.path.join(filepath, "pdftron_wrap.cxx")
    with open(filepathname, "w+") as f:
       f.write(cxx)

    filepathname = os.path.join(filepath, "pdftron_wrap.h")
    with open(filepathname, "w+") as f:
       f.write(h)

    filepathname = os.path.join(filepath, "pdftron.go")
    with open(filepathname, "w+") as f:
       f.write(go)

def copyPaths(prefix, srcPaths, dest):
    for path in srcPaths:
        print("Copying %s/%s to %s..." % (prefix, path, dest))
        copytree(os.path.join(prefix, path), os.path.join(dest, path))

def extractArchive(fileName):
    ext = path(fileName)
    ext = ''.join(ext.suffixes)
    if ext == ".tar.gz":
        tarfile.open(fileName).extractall();
    else:
        with zipfile(fileName, 'r') as archive:
            archive.extractall()

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-dl', '--download_link', dest='dl', default='')
    parser.add_argument('-wr', '--wrapper', dest='wr', default='BUILD_PDFTronGo')
    parser.add_argument('-cs', '--custom_swig', dest='custom_swig', default='')
    # skips nightly pull
    parser.add_argument('-sdl', '--skip_dl', dest='skip_dl', action='store_true')

    stored_args, ignored_args = parser.parse_known_args()

    core_download_link = stored_args.dl
    wrapper = stored_args.wr
    custom_swig = stored_args.custom_swig
    skip_dl = stored_args.skip_dl

    rootDir = os.getcwd()
    try:
        shutil.rmtree("build", ignore_errors=True)
    except FileNotFoundError:
        pass
    os.mkdir("build")
    # provided by repo
    os.chdir("PDFNetC")

    gccCommand = ""
    cmakeCommand = "cmake -D BUILD_%s=ON" % wrapper
    if custom_swig:
        swigVersionCommand = "%s -version" % custom_swig
        result = subprocess.run([custom_swig, '-version'], stdout=subprocess.PIPE)
        swigVersion = re.search(r"\d+\.\d+\.\d+", result.stdout.decode()).group()
        print("Using custom SWIG at %s, version %s" % (custom_swig, swigVersion))
        cmakeCommand += " -D CUSTOM_SWIG=%s -D SWIG_VERSION=%s" % (custom_swig, swigVersion)

    cmakeCommand += ' ..'

    if wrapper.endswith('PDFTronGo'):
        entryPoint = "pdftron_wrap.cxx"
        entryHeader = "pdftron_wrap.h"
        entryPath = os.path.join(wrapper, "pdftron")
    elseif wrapper.endswith('PDFTronPHP'):
        entryPoint = "PDFNetPHP.cpp"
        entryHeader = "PDFNetPHP.hpp"
        entryPath = wrapper

    if platform.system().startswith('Windows'):
        print("Running Windows build...")
        if not core_download_link:
           core_download_link = 'http://www.pdftron.com/downloads/PDFNetC64.zip'
        if not skip_dl:
           print("Downloading PDFNetC64...")
           urllib.request.urlretrieve(core_download_link, "PDFNetC64.zip")
        extractArchive("PDFNetC64.zip")
        os.remove("PDFNetC64.zip")
        copyPaths('PDFNetC64', ['Headers', 'Lib'], '.')
        cmakeCommand = 'cmake -G "MinGW Makefiles" -D BUILD_%s=ON ..' % wrapper
        gccCommand = "g++ -shared -I../Headers -L . -lPDFNetC %s -o pdftron.dll" % entryPoint
    elif platform.system().startswith('Linux'):
        print("Running Linux build...")
        if not core_download_link:
           core_download_link = 'http://www.pdftron.com/downloads/PDFNetC64.tar.gz'
        print(core_download_link)
        if not skip_dl:
           print("Downloading PDFNetC64...")
           urllib.request.urlretrieve(core_download_link, 'PDFNetC64.tar.gz')
        extractArchive("PDFNetC64.tar.gz")
        os.remove("PDFNetC64.tar.gz")
        copyPaths('PDFNetC64', ['Headers', 'Lib'], '.')
        gccCommand = "g++ -fuse-ld=gold -fpic -I ../Headers -L . -lPDFNetC -Wl,-rpath,. -shared -static-libstdc++ %s -o libpdftron.so" % entryPoint
    else:
        print("Running Mac build...")
        if not core_download_link:
           core_download_link = 'http://www.pdftron.com/downloads/PDFNetCMac.zip'
        if not skip_dl:
           print("Downloading PDFNetC64...")
           urllib.request.urlretrieve(core_download_link, 'PDFNetCMac.zip')

        extractArchive("PDFNetCMac.zip")
        os.remove("PDFNetCMac.zip")
        copyPaths('PDFNetCMac', ['Headers', 'Lib', 'Resources'], '.')
        gccCommand = "gcc -fPIC -lstdc++ -I../Headers -L. -lPDFNetC -dynamiclib -undefined suppress -flat_namespace %s -o libpdftron.dylib" % entryPoint

    os.chdir("../build")

    print("Starting cmake: " + cmakeCommand)
    try:
        for data in execute(cmakeCommand):
           print(data, end="")
    except subprocess.CalledProcessError as e:
        if e.stdout is None:
            print(str(e.stdout));
        else:
            print(e.stdout.decode())
        raise

    print("Moving pdftron wrap...")
    os.chdir(entryPath)

    if wrapper.endswith('PDFTronGo'):
        if platform.system().startswith('Windows'):
            shutil.copy(os.path.join(rootDir, "PDFTronGo", "CI", "Windows", "pdftron.go.replace"), '.')
            shutil.copy(os.path.join(rootDir, "PDFTronGo", "CI", "Windows", "pdftron_wrap.cxx.replace"), '.')
            shutil.copy(os.path.join(rootDir, "PDFTronGo", "CI", "Windows", "pdftron_wrap.h.replace"), '.')
            replacego('.')

    shutil.move(entryPoint, os.path.join("PDFNetC", "Lib"))
    shutil.move(entryHeader, os.path.join("PDFNetC", "Lib"))

    os.chdir(os.path.join("PDFNetC", "Lib"))
    if platform.system().startswith('Windows'):
        os.remove("pdfnetc.lib")

    print("Running GCC: " + gccCommand)
    try:
        for data in execute(gccCommand):
           print(data, end="")

    except subprocess.CalledProcessError as e:
        if e.stdout is None:
            print(str(e.stdout));
        else:
            print(e.stdout.decode())
        raise

    print("Build completed.")
    return 0

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

if __name__ == '__main__':
    main()
