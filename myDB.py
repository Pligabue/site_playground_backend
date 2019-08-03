import mysql.connector

def sqlChange(sqlFormula, sqlTuple):

    try:

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

        print("SUCCESS")
        return True

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False
        

def sqlQuery(sqlFormula):

    try:

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

        print("SUCCESS")
        return data

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False
