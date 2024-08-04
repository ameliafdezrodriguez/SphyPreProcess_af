import subprocess, traceback
from qgis.PyQt import QtCore

#-Class to run subprocess in a thread
class SubProcessWorker(QtCore.QObject):
    '''Example worker'''
    finished = QtCore.pyqtSignal(object)
    error = QtCore.pyqtSignal(Exception, str)
    cmdProgress = QtCore.pyqtSignal(object)
    #- commands are required. If the worker is about a map creation, then the following is required: 
    # mapname, filename, added to canvas (True or False), and ftype ('raster' or 'shape')
    def __init__(self, commands, textLog, mapname=None, filename=None, addmap=None, ftype=None, env=None):
        QtCore.QObject.__init__(self)
        self.commands = commands
        self.mapName = mapname
        self.fileName = filename
        self.addMap = addmap
        self.fType = ftype
        self.env = env
        self.textLog = textLog  # required to know to which text log in the GUI append the processing text log

    def run(self):
        self.cmdProgress.emit(["--------------------------------------", self.textLog])
        try:  #-execute each individual command in a separate subprocess
            for command in self.commands:

                self.result = subprocess.run(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=self.env,
                    check= True
                )

                if self.result.returncode != 0:
                    self.cmdProgress.emit([f"Command '{command}' failed with return code {self.result.returncode}", self.textLog])
                    self.cmdProgress.emit([self.result.stderr, self.textLog])
                else:
                    self.cmdProgress.emit([f"Command '{command}' completed successfully", self.textLog])
                    self.cmdProgress.emit([self.result.stdout, self.textLog])

            self.cmdProgress.emit(["Loop completed", self.textLog])

            # Send signal
            self.finished.emit([self.result, self.mapName, self.fileName, self.addMap, self.fType, self.textLog])
            self.cmdProgress.emit(["Sent signal", self.textLog])


        except Exception as e:
            # forward the exception upstream
            self.error.emit(e, traceback.format_exc())
