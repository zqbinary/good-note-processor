from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to my Python Web Service!"

if __name__ == '__main__':
    app.run(debug=True)
