import jpype
from pathlib import Path

def startJVM(classpath = None, rootdir = "../", debug=False):
    if classpath is None:
        dirs = ["daccad/build/dist/lib/*","/daccad/build/libs/daccad-*.jar","daccad/build/classes/java/main"]
        classpath = [Path(rootdir,d).resolve() for d in dirs]
    if debug:
        print("Classpath:",classpath)
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath = classpath)
    return classpath