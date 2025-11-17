from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Testing"

# test push
if __name__ == "__main__":
    app.run(debug=True)