# TODO: comment functions

# iris import to handle iris connections
import iris

# connection by iris
# TODO: make it changeable by the client side
connection_string = 'localhost:1972/%SYS'
username = '_system'
password = 'SYS'
connection = iris.connect(connection_string, username, password)
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


# def getGlobalAllocatedSize(databaseDirectory: str, globalName: str):
#     try:
#         allocatedSize = iris.IRISReference(0)
#         status = irispy.classMethodObject("%Library.GlobalEdit", "GetGlobalSize", databaseDirectory, globalName, globalName, allocatedSize)
#         if (status != 1):
#             #TODO: get error text
#             statusText = irispy.classMethodString("%SYSTEM.Status", "GetErrorText", status)
#             raise Exception(statusText)

#     except Exception as error:
#         return str(error)

#     return allocatedSize.getValue()


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
        # TODO: verify namespace
        statement = irispy.classMethodObject("%SQL.Statement", "%New")
        status = statement.invoke("%Prepare", "SELECT DISTINCT Directory FROM Config.Databases WHERE SectionHeader = 'Databases'")

        if (status != 1):
            statusText = irispy.classMethodString("%SYSTEM.Status", "GetErrorText", status)
            raise Exception(statusText)

        result = statement.invoke("%Execute")

        databaseDirectoriesList = []
        while (result.invoke("%Next")!=0):
            databaseDirectoriesList.append(result.invoke("%Get", "Directory"))

    except Exception as error:
        return str(error)

    return databaseDirectoriesList


