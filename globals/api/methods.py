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

    return globalUsed.getValue(), globalAllocated.getValue()

def getGlobalsList(databaseDirectory: str, databaseName: str):
    try:
        statement = irispy.classMethodObject("%SQL.Statement", "%New")
        status = statement.invoke("%PrepareClassQuery", "%SYS.GlobalQuery","DirectoryList")
        if (status != 1):
            statusText = irispy.classMethodString("%SYSTEM.Status", "GetErrorText", status)
            raise Exception(statusText)

        result = statement.invoke("%Execute", databaseDirectory)
        

        globalList = []
        tableList = []
        while (result.invoke("%Next")!=0):
            globalName = result.invoke("%Get", "Name")
            tableName = irispy.classMethodValue("%ExtentMgr.Util", "GlobalToSqlTable", databaseName, "^"+globalName, status)
            if tableName==None:
                tableName = ""

            globalList.append(globalName)
            tableList.append(tableName)

    except Exception as error:
        return str(error)

    return globalList, tableList


def getAllDatabaseDirectories():
    try:
        # check the connection made in irisPy, and if it is set to %SYS namespace
        databaseDirectoriesList = []
        databaseNameList = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT %EXACT(Directory), Name FROM Config.Databases WHERE SectionHeader = ?", ["Databases",],)
            
            for row in cursor:
                databaseDirectoriesList.append(row[0])
                databaseNameList.append(row[1])

    except Exception as error:
        return str(error)

    return databaseDirectoriesList, databaseNameList


