# TODO: comment functions

# iris import to handle iris connections
import intersystems_iris as iris
from django.db import connection as djangoconnection


# connection by iris
conn_params = djangoconnection.get_connection_params()
conn_params["namespace"] = "%SYS"
connection = iris.connect(**conn_params)
irispy = iris.createIRIS(connection)

def getProcessList():
    try:
        statement = irispy.classMethodObject("%SQL.Statement", "%New")
        status = statement.invoke("%PrepareClassQuery", "%SYS.ProcessQuery","AllFields")
        if (status != 1):
            statusText = irispy.classMethodString("%SYSTEM.Status", "GetErrorText", status)
            raise Exception(statusText)

        result = statement.invoke("%Execute")

        processList = []
        while (result.invoke("%Next")!=0):
            process = {}

            process["jobNumber"] = result.invoke("%Get", "JobNumber")
            process["pid"] = result.invoke("%Get", "Pid")
            process["osUserName"] = result.invoke("%Get", "OSUserName")
            process["currentDevice"] = result.invoke("%Get", "CurrentDevice")
            process["routine"] = result.invoke("%Get", "Routine")
            process["state"] = result.invoke("%Get", "State")
            process["userName"] = result.invoke("%Get", "UserName")

            processList.append(process)

    except Exception as error:
        return str(error)

    return processList
