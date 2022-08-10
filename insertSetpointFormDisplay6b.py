# importing Flask and other modules
from flask import Flask, request, render_template

# python imports
import requests


# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function
@app.route('/' , methods =["GET", "POST"])
def formDisplay():
    output = ""                 # display nothing if form is not submitted
    if request.method == 'POST':                                               # procees HTTP POST
        strIOTSensorLocation =  request.form['IOTSensorLocation']         # gets the form key / value pair - gets the value for 'IOTSensorLocation'
        strMeasurement =  request.form['Measurement']                 # gets the form key / value pair - gets the value for 'Measurement'
        strSetpoint =  request.form['Setpoint']                 # gets the form key / value pair - gets the value for 'username'
        strDeadband = request.form['Deadband']

    # query database and return result (value)
        try:
            url = "http://3.25.198.226/i40Test/v5/RPIsetpointInsertV5.php" 
            #url = "http://localhost/i40Test/php/v5/RPIsetpointInsertV5.php" 
            contentJson= { "IOTSensorLocation" : strIOTSensorLocation, "Measurement" : strMeasurement, "Setpoint": strSetpoint, "Deadband": strDeadband }
            r = requests.post(url,data = contentJson) # works for local and AWS
            # print(r.text)
            responseData = r.json()
            print(responseData) # for debugging
            if "Value" in responseData:
                pass                    # value is returned from measured data table
            else:                       # no value in measuredata Table
                responseData = {'code':'502', 'Value' : 0 , 'message' : 'No Value', 'IOTSensorLocation': strIOTSensorLocation , 'Measurement': strMeasurement, 'Setpoint' : strSetpoint , 'Deadband' : strDeadband}    # format as a string 
        except requests.ConnectionError as err:
            responseData = {'code':'501', 'Value' : -1 , 'message' : '{}'.format(err), 'IOTSensorLocation': '00000000' , 'Measurement': 'Temperature', 'Setpoint' : 21 , 'Deadband' : 2}    # format as a string 


        # 
    else :
        strIOTSensorLocation =  "13111111"         # gets the form key / value pair - gets the value for 'IOTSensorLocation'
        strMeasurement =  "Humidity"                 # gets the form key / value pair - gets the value for 'Measurement'
        strSetpoint =  "50"                 # gets the form key / value pair - gets the value for 'username'
        strDeadband = "10"
        value = 0
        responseData = {'code':'500', 'message' : 'GET', 'IOTSensorLocation': strIOTSensorLocation , 'Measurement': strMeasurement, 'Setpoint' : strSetpoint , 'Deadband' : strDeadband, 'Value' : value}    # format as a string 

    # output data in Json format
    contentJson= { "IOTSensorLocation" : strIOTSensorLocation, "Measurement" : strMeasurement, "Setpoint": strSetpoint, "Deadband": strDeadband }

    print(contentJson)
    print(responseData)

    # data to be displayed in form
    templateData = {
        'Value' : responseData["Value"],
        'IOTSensorLocation' : responseData["IOTSensorLocation"],
        'Measurement' : responseData["Measurement"],
        'Setpoint' : responseData["Setpoint"],
        'Deadband' : responseData["Deadband"],
        'test' : '100'      # issue with this displaying should be measured value
        }
            
    return render_template("insertSetpointFormDisplay4b.html", **templateData)   


if __name__=='__main__':
    app.run("0.0.0.0" , debug=True)
