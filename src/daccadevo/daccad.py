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

#def startDACCAD(debug=False):
#    rootdir = startJVM(debug=debug)
    # Example usage
    #import model.Constants
    #import model.OligoGraph
    #import model.OligoSystem
    #import model.chemicals.SequenceVertex
    #import utils.GraphUtils
    
    # g = utils.GraphUtils.initGraph()

    # print(jpype.JPackage('model.Constants'))
    # print(java.lang.System.getProperty('java.class.path'))
    # jpype.JPackage('model.OligoGraph')
    # jpype.JPackage('model.OligoSystem')
    # jpype.JPackage('model.chemicals.SequenceVertex')
    # jpype.JPackage('utils.GraphUtils')

#if __name__ == "__main__":
#    startDACCAD(debug=True)