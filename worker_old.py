# The SPHY model Pre-Processor interface plugin for QGIS:
# A QGIS plugin that allows the user to create SPHY model input data based on a database. 
#
# Copyright (C) 2015  Wilco Terink
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email: w.terink@futurewater.nl OR terinkw@gmail.com

#-Authorship information-###################################################################
__author__ = "Wilco Terink"
__copyright__ = "Wilco Terink"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "w.terink@futurewater.nl, terinkw@gmail.com"
__date__ ='1 January 2017'
############################################################################################

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
        self.process = None
        self.mapName = mapname
        self.fileName = filename
        self.addMap = addmap
        self.fType = ftype
        self.env = env
        self.textLog = textLog  # required to know to which text log in the GUI append the processing text log

    def run(self):
        try:#-execute each individual command in a separate subprocess
            for command in self.commands:
                self.process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=False,
                    env=self.env
                    ).wait()
                  
                #proc = self.process.stdout

                # while True:
                #     line = proc.readline()
                #     if not line:
                #         print("No more lines to read.")
                #         break
                #     print(f"Read line: {line}")
                #     if "Traceback" in line:
                #         self.process = None
                #         break
                #     elif "WARNING" in line or "temp" in line or "ERROR" in line or "Permission" in line:
                #         self.cmdProgress.emit(['...', self.textLog])
                #     else:
                #         self.cmdProgress.emit([line, self.textLog])
                self.cmdProgress.emit([command, self.textLog])
                self.cmdProgress.emit(["Waiting for process to complete.", self.textLog])
                #self.process.wait()  # Wait for the process to complete
                self.cmdProgress.emit(["Process completed", self.textLog])

            # Send signal
            print('Sent signal')
            self.cmdProgress.emit(["Sent signal", self.textLog])
            
            print('Emitting....')
            self.finished.emit([self.process, self.mapName, self.fileName, self.addMap, self.fType, self.textLog])
            print('Emitted....')

                
        except Exception as e:
            # forward the exception upstream
            self.error.emit(e, traceback.format_exc())
        

         
