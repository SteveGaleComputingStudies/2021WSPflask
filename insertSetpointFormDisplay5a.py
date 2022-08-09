# importing Flask and other modules
from flask import Flask, request, render_template

# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function
@app.route('/' , methods =["GET", "POST"])
def formDisplay():
    output = ""                 # display nothing if form is not submitted
    if request.method == 'POST':                         # procees HTTP POST
        strIOTSensorLocation =  request.form['IOTSensorLocation']         # gets the form key / value pair - gets the value for 'IOTSensorLocation'
        strMeasurement =  request.form['Measurement']                 # gets the form key / value pair - gets the value for 'Measurement'
        strSetpoint =  request.form['Setpoint']                 # gets the form key / value pair - gets the value for 'username'
        strDeadband = request.form['Deadband']

    # query database and return most recent MeasuredData result (value)

        value = int(strSetpoint)+ int(strDeadband)          # for testing
    else :                                                  # get request
        strIOTSensorLocation =  "13111111"         # gets the form key / value pair - gets the value for 'IOTSensorLocation'
        strMeasurement =  "Humidity"                 # gets the form key / value pair - gets the value for 'Measurement'
        strSetpoint =  "50"                 # gets the form key / value pair - gets the value for 'username'
        strDeadband = "10"
        value = 21

    # data to be displayed in form
    templateData = {
        'Value' : value,
        'IOTSensorLocation' : strIOTSensorLocation,
        'Measurement' : strMeasurement,
        'Setpoint' : strSetpoint,
        'Deadband' : strDeadband,
        'test' : '100'      # issue with this displaying should be measured value
        }
            
    return render_template("insertSetpointFormDisplay4b.html", **templateData)   


if __name__=='__main__':
    app.run("0.0.0.0" , debug=True)
