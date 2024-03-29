# 2022 WSP database crud
# run the python file (VScode - Run Python File in Terminal) amd run ex9test.py in idle to POST json Data
# change the Id value in the browser Url and refresh
# ref - https://flask.palletsprojects.com/en/2.0.x/quickstart/#apis-with-json
# ref - https://www.geeksforgeeks.org/python-sqlite-working-with-date-and-datetime/
# ref - https://www.sqlitetutorial.net/sqlite-python/insert/
# https://www.sqlite.org/autoinc.html


#import sqlite3
#from sqlite3 import Error
import datetime
from flask import Flask, request, jsonify , redirect , url_for, render_template, Response 

import io
import csv
import requests


app = Flask(__name__)

# mysql code
import mysql.connector
mySQLdb2022 = "2022industry40db"

@app.route('/api/v1/selectSetpointWHEREMySQL/', methods=['GET', 'POST'])
def dBselectSetpointWHEREMySQL():
    # 
    # default response if no post
    responseData = {'code':'200', 'message' :'OK', 'IOTSensorLocation': '13111111' , 'Measurement': 'Temperature', 'Setpoint' : 21 , 'Deadband' : 2, 'Value' : 0}

    if request.method == 'POST':                                               # procees HTTP POST
        strIOTSensorLocation =  request.form['IOTSensorLocation']         # gets the form key / value pair - gets the value for 'IOTSensorLocation'
        strMeasurement =  request.form['Measurement']                 # gets the form key / value pair - gets the value for 'Measurement'
              # gets the form key / value pair - gets the value for 'username'
    # replace this with POST reqiest to AWS V5 , return JSON data to populate template
        try:
            conn = mysql.connector.connect(host="localhost", user="I40", passwd="Password1",database= mySQLdb2022)

            # added for V5
            stmtSelect = "SELECT * FROM MeasuredDataV3 WHERE IOTSensorLocation = %s AND Measurement = %s ORDER BY readdate DESC "
            cur = conn.cursor() # removed prepared=True
            cur.execute(stmtSelect, (strIOTSensorLocation, strMeasurement ))
            data = cur.fetchall()

        #
            for row in data:
                print(" {}  {}  {} ".format(row[0],row[1],row[2]))

        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            return jsonify({'code':'500', 'message' : '{}'.format(err)})

        finally:
            if conn:
                conn.close()
        return render_template('displayMeasuredData8b.html', output_data = data)                             # procees HTTP GET - render ex5.html if not yet logged in om templates folder in project

    else:
        templateData = {
            'IOTSensorLocation' : responseData["IOTSensorLocation"],
            'Measurement' : responseData["Measurement"],
            'test' : '100'      # issue with this displaying should be measured value
           }
            
        return render_template("selectMeasuredDataFormDisplay9b.html", **templateData)                              # procees HTTP GET - render ex5.html if not yet logged in om templates folder in project


@app.route('/api/v1/selectMeasuredData/')
def dBselectMeasuredData():
    try: 
        conn = mysql.connector.connect(host="localhost", user="I40", passwd="Password1",database= mySQLdb2022)
        cur = conn.cursor()

        cur.execute('SELECT * FROM MeasuredDataV3 ORDER BY readDate DESC')
        data = cur.fetchall()

        #
        for row in data:
            print(" {}  {}  {} ".format(row[0],row[1],row[2]))

    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        return jsonify({'code':'500', 'message' : '{}'.format(err)})

    finally:
        if conn:
            conn.close()
    return render_template('displayMeasuredData8b.html', output_data = data)
# https://stackoverflow.com/questions/45558349/flask-display-database-from-python-to-html


@app.route('/api/v1/selectSetpoints/')
def dBselectSetpoints():
    try: 
        conn = mysql.connector.connect(host="localhost", user="I40", passwd="Password1",database= mySQLdb2022)
        cur = conn.cursor()

        cur.execute('SELECT * FROM SetpointsV3 ORDER BY setDate DESC')
        data = cur.fetchall()

        #
        for row in data:
            print(" {}  {}  {} ".format(row[0],row[1],row[2]))

    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        return jsonify({'code':'500', 'message' : '{}'.format(err)})

    finally:
        if conn:
            conn.close()
    return render_template('displayMeasuredData8b.html', output_data = data)
# https://stackoverflow.com/questions/45558349/flask-display-database-from-python-to-html


@app.route('/api/v1/createMySQLdb/', methods=['GET', 'POST'])
def dBcreateMySQLdb():
    try: 
        conn = mysql.connector.connect(host="localhost", user="I40", passwd="Password1")
        cur = conn.cursor()
        sqlCreateDb = "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(mySQLdb2022)
        cur.execute(sqlCreateDb)
        responseData = {'code':'200', 'message' :'OK - db created'}
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        responseData = {'code':'500', 'message' : '{}'.format(err)}
    finally:
        if conn:
            conn.close()
    return jsonify(responseData)
#http://localhost:5000/api/v1/createMySQLdb/    
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html

@app.route('/api/v1/createMySQLtableSetpoints/', methods=['GET', 'POST'])
def dBcreateMySQLtableSetpoints():
    try: 
        conn = mysql.connector.connect(host="localhost", user="I40", passwd="Password1",database= mySQLdb2022)
        cur = conn.cursor() # removed prepared=True
        sqlCreateTableSetpoints = "CREATE TABLE SetpointsV3 (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, IOTSensorLocation VARCHAR(20) NOT NULL,Measurement VARCHAR(16),Setpoint VARCHAR(8),Deadband VARCHAR(8), setDate TIMESTAMP)"
        cur.execute(sqlCreateTableSetpoints)
        responseData = {'code':'200', 'message' :'OK - Table created'}
    except mysql.connector.Error as err:
        print("Failed creating table: {}".format(err))
        responseData = {'code':'500', 'message' : '{}'.format(err)}
    finally:
        if conn:
            conn.close()
    return jsonify(responseData)
# http://localhost:5000/api/v1/createMySQLtableSetpoints/  
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html

@app.route('/api/v1/createMySQLtableMeasuredData/', methods=['GET', 'POST'])
def dBcreateMySQLtableMeasuredData():
    try: 
        conn = mysql.connector.connect(host="localhost", user="I40", passwd="Password1",database= mySQLdb2022)
        cur = conn.cursor() # removed prepared=True
        sqlCreateTableMeasuredData = "CREATE TABLE MeasuredDataV3 (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, IOTSensorLocation VARCHAR(20) NOT NULL, Measurement VARCHAR(16), Value VARCHAR(8), readDate TIMESTAMP )"
        cur.execute(sqlCreateTableMeasuredData)
        responseData = {'code':'200', 'message' :'OK - Table created'}
    except mysql.connector.Error as err:
        print("Failed creating table: {}".format(err))
        responseData = {'code':'500', 'message' : '{}'.format(err)}
    finally:
        if conn:
            conn.close()
    return jsonify(responseData)
# http://localhost:5000/api/v1/createMySQLtableMeasuredData/  


@app.route('/api/v1/insertSetpointMySQL/', methods=['GET', 'POST'])
def dBinsertSetpointMySQL():
    # 
    # default response if no post
    responseData = {'code':'200', 'message' :'OK', 'IOTSensorLocation': '13111111' , 'Measurement': 'Temperature', 'Setpoint' : 21 , 'Deadband' : 2, 'Value' : 0}

    if request.method == 'POST':                                               # procees HTTP POST
        strIOTSensorLocation =  request.form['IOTSensorLocation']         # gets the form key / value pair - gets the value for 'IOTSensorLocation'
        strMeasurement =  request.form['Measurement']                 # gets the form key / value pair - gets the value for 'Measurement'
        strSetpoint =  request.form['Setpoint']                 # gets the form key / value pair - gets the value for 'username'
        strDeadband = request.form['Deadband']
              # gets the form key / value pair - gets the value for 'username'
    # replace this with POST reqiest to AWS V5 , return JSON data to populate template
        try:
            conn = mysql.connector.connect(host="localhost", user="I40", passwd="Password1",database= mySQLdb2022)
            cur = conn.cursor() # removed prepared = true
            # https://stackoverflow.com/questions/60752474/how-to-insert-value-into-date-column-in-mysql-table-from-python-3
            # setDate required for python insert as NOW() doesnt work in query as per PHP
            strDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            stmt = "INSERT INTO SetpointsV3 (IOTSensorLocation, Measurement, Setpoint, Deadband , setDate ) VALUES (%s, %s, %s, %s, %s)"
            #https://stackoverflow.com/questions/34046634/insert-into-a-mysql-database-timestamp
            cur.execute(stmt, (strIOTSensorLocation, strMeasurement, strSetpoint , strDeadband ))

            # added for V5
            stmtSelect = "SELECT Value FROM MeasuredDataV3 WHERE IOTSensorLocation = %s AND Measurement = %s ORDER BY readdate DESC LIMIT 1"
            cur = conn.cursor() # removed prepared=True
            cur.execute(stmtSelect, (strIOTSensorLocation, strMeasurement ))
            rows = cur.fetchone() #cur.fetchall()

            if rows == None:        # no MeasuredData for this IOTSensorLocation
                responseData = {'code':'200', 'message' :'OK', 'IOTSensorLocation': strIOTSensorLocation , 'Measurement': strMeasurement, 'Setpoint' : '20' , 'Deadband' : '0', 'Value' : 0}
            else :
                measuredValue = rows[0] # redundant
                responseData = {'code':'200', 'message' :'OK', 'IOTSensorLocation': strIOTSensorLocation , 'Measurement': strMeasurement, 'Setpoint' : strSetpoint , 'Deadband' : strDeadband, 'Value' : rows[0]}
            conn.commit()
        except mysql.connector.Error as err:
            responseData = {'code':'500', 'Value' : -1 , 'message' : '{}'.format(err)}    # format as a string 
        finally:
            if conn:
                conn.close()

    templateData = {
        'Value' : responseData["Value"],
        'IOTSensorLocation' : responseData["IOTSensorLocation"],
        'Measurement' : responseData["Measurement"],
        'Setpoint' : responseData["Setpoint"],
        'Deadband' : responseData["Deadband"],
        'test' : '100'      # issue with this displaying should be measured value
        }
            
    return render_template("insertSetpointFormDisplay9a.html", **templateData)                              # procees HTTP GET - render ex5.html if not yet logged in om templates folder in project
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursorprepared.html
# https://stackoverflow.com/questions/60752474/how-to-insert-value-into-date-column-in-mysql-table-from-python-3
# http://localhost:5000/api/v1/insertSetpointMySQL/  

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")    


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)         # allow connections from remote client
