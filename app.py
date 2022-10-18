from ast import main
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/json")
def JsonData():
    return "<p>Returning JSON data</p>"
    
@app.route("/proto")
def ProtoData():
    return "<p>Returning binary data</p>"

if __name__ == "__main__":
    app.run(debug=True)  