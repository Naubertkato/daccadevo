import jpype
import jpype.imports
from jpype.types import *

def startJVM(classpath = None, debug=False):
    if classpath is None:
        import os
        dirs = ["daccad/build/dist/lib/*","/daccad/build/libs/daccad-1.5.0.jar","daccad/build/classes/java/main"]
        rootdir = os.path.dirname(os.path.abspath(__file__))
        # Go up then 
        rootdir = os.path.dirname(os.path.dirname(rootdir))
        classpath = [os.path.join(rootdir,d) for d in dirs]
    if debug:
        print("Classpath:",classpath)
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath = classpath)
    return rootdir

def startDACCAD(debug=False):
    rootdir = startJVM(debug=debug)
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

if __name__ == "__main__":
    startDACCAD(debug=True)