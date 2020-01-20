from org.apache.nifi.processors.script import ExecuteScript
from org.apache.nifi.processor.io import InputStreamCallback
from java.io import BufferedReader, InputStreamReader
from org.apache.nifi.components.state import Scope
import numpy as np

class ReadFirstLine(InputStreamCallback) :
    __line = None;

    def __init__(self) :
        pass

    def getLine(self) :
        return self.__line

    def process(self, input) :
        try :
            reader = InputStreamReader(input)
            bufferedReader = BufferedReader(reader)
            self.__line = bufferedReader.readLine()
        except :
            print "Exception in Reader:"
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60
            raise
        finally :
            if bufferedReader is not None :
                bufferedReader.close()
            if reader is not None :
                reader.close()

flowFile = session.get()

if flowFile is not None :
    stateManager = context.stateManager
    stateMap = stateManager.getState(Scope.LOCAL)
    newMap = {"pi": str(np.pi)}
    # for k, v in vars().items():
    #     if not (k.startswith('__') and k.endswith('__')):
    #         newMap[k] = v
    #newMap = {'myKey1': 'myValue1'}
    stateManager.setState(newMap, Scope.LOCAL)
    reader = ReadFirstLine()
    session.read(flowFile, reader)
    flowFile = session.putAttribute(flowFile, "from-content", "dehy")
    session.transfer(flowFile, ExecuteScript.REL_SUCCESS)