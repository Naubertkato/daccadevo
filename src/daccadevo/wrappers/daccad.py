from pathlib import Path

import jpype


def startJVM(classpath = None, rootdir = "../daccad", jvmpath=None, verbose=False):
    """Start the JVM for DACCAD simulations.

    The function sets the proper classpath for DACCAD dependencies, starts the JVM,
    and returns the classpath.
    If the JVM is already started, only returns the full classpath.

    Parameters
    ----------
    classpath: list of str or Path, optional, default is None
        Paths to the DACCAD jar file, compiled classes, and dependencies.
        If not `None`, used as absolute paths, passed to the JVM through JPype.
        If `None`, defaults to `["build/dist/lib/*","build/libs/daccad-*.jar","build/classes/java/main"]`
        (the default DACCAD structure) under `rootdir`.
    rootdir: str or Path, default is `"../daccad"`
        Path of the root directory of DACCAD. Only used if `classpath` is `None`.
    jvmpath: str or Path, optional, default is None
        Path to the JVM, forwarded to JPype. If `None`, the system default is used.
    verbose: bool, default is `False`
        Toggle a print of the classpath as provided to JPype.

    Returns
    -------
    classpath: list of Path
        The classpath as provided to JPype
    """
    if classpath is None:
        dirs = ["build/dist/lib/*","build/libs/daccad-*.jar","build/classes/java/main"]
        classpath = [Path(rootdir,d).resolve() for d in dirs]
    
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath = classpath, jvmpath=jvmpath)
    else:
        classpath = [Path(str(d)) for d in jpype.java.lang.System.getProperty('java.class.path').split(":")]
    if verbose:
        print("Classpath:",classpath)
    return classpath
