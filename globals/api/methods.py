# TODO: comment functions

# iris import to handle iris connections
import intersystems_iris as iris
from django.db import connection as djangoconnection


# connection by iris
conn_params = djangoconnection.get_connection_params()
conn_params["namespace"] = "%SYS"
connection = iris.connect(**conn_params)
irispy = iris.createIRIS(connection)


def getGlobalSize(databaseDirectory: str, globalName: str):
    try:
        globalUsed = iris.IRISReference(0)
        globalAllocated = iris.IRISReference(0)
        status = irispy.classMethodObject("%GlobalEdit", "GetGlobalSize", databaseDirectory, globalName, globalAllocated, globalUsed, 0)
        if (status != 1):
            #TODO: get error text
            statusText = irispy.classMethodString("%SYSTEM.Status", "GetErrorText", status)
            raise Exception(statusText)

    except Exception as error:
        return str(error)

    return (globalUsed.getValue(), globalAllocated.getValue())

def getGlobalsList(databaseDirectory: str):
    try:
        statement = irispy.classMethodObject("%SQL.Statement", "%New")
        status = statement.invoke("%PrepareClassQuery", "%SYS.GlobalQuery","DirectoryList")
        if (status != 1):
            statusText = irispy.classMethodString("%SYSTEM.Status", "GetErrorText", status)
            raise Exception(statusText)

        result = statement.invoke("%Execute", databaseDirectory)

        globalList = []
        while (result.invoke("%Next")!=0):
            globalList.append(result.invoke("%Get", "Name"))

    except Exception as error:
        return str(error)

    return globalList


def getAllDatabaseDirectories():
    try:
        # check the connection made in irisPy, and if it is set to %SYS namespace
        databaseDirectoriesList = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT %EXACT(Directory) FROM Config.Databases WHERE SectionHeader = ?", ["Databases",],)
            databaseDirectoriesList = [row[0] for row in cursor]

    except Exception as error:
        return str(error)

    return databaseDirectoriesList


