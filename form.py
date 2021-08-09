# importing Flask and other modules
from flask import Flask, request, render_template

# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function
@app.route('/' , methods =["GET", "POST"])
def displayForm():
    output = ""                 # display nothing if form is not submitted
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
# SELECT * from users Where Firstname = 

        output =  "Your name is "+ first_name + " " + last_name

    # data to be displayed in form
    templateData = {
        "title" : "test form 1",
        "responseText" : output
    }
    return render_template("form.html", **templateData)

if __name__=='__main__':
    app.run()
