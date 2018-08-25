import pymysql.cursors

dbServerName = "localhost"
dbUser = "root"
dbPassword = "woodycool123"
dbName = "azure_support_tweets"
cusrorType = pymysql.cursors.DictCursor

connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset='utf8mb4', cursorclass=cusrorType)

try:
    # Create a cursor object
    cursorObject = connectionObject.cursor()

    # SQL query string
    sqlQuery = "CREATE TABLE Employee(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)

    # SQL query string
    sqlQuery = "show tables"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)

    #Fetch all the rows
    rows = cursorObject.fetchall()
    for row in rows:
        print(row)

except Exception as e:
    print("Exeception occured:{}".format(e))

finally:
    connectionObject.close()