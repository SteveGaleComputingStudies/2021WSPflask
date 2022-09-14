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



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")    


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)         # allow connections from remote client
