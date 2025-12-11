import jpype
from pathlib import Path

def startJVM(classpath = None, rootdir = "../daccad", jvmpath=None, debug=False):
    if classpath is None:
        dirs = ["build/dist/lib/*","build/libs/daccad-*.jar","build/classes/java/main"]
        classpath = [Path(rootdir,d).resolve() for d in dirs]
    if debug:
        print("Classpath:",classpath)
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath = classpath, jvmpath=jvmpath)
    return classpath