import mysql.connector

def sqlChange(sqlFormula, sqlTuple):

    mydb = mysql.connector.connect (
        host="localhost",
        user="root",
        passwd="senha123",
        database="site_playground"
    )

    mycursor = mydb.cursor()
    
    mycursor.execute(sqlFormula, sqlTuple)

    mydb.commit()

    mydb.close()

def sqlQuery(sqlFormula):

    mydb = mysql.connector.connect (
        host="localhost",
        user="root",
        passwd="senha123",
        database="site_playground"
    )

    mycursor = mydb.cursor()
    
    mycursor.execute(sqlFormula)

    data = mycursor.fetchall()

    mydb.close()

    return data