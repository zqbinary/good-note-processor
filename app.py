from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

from service.HtmlProcessor import HtmlProcessor

app = Flask(__name__)
# CORS(app, resources={r"/html": {"origins": "*"}}, supports_credentials=True)
# CORS(app, resources=r'/*')
CORS(app)


@app.route('/')
def index():
    return render_template('t1.html')


@app.route('/out')
def index2():
    return render_template('out.html')


@app.route('/html', methods=['POST'])
def html():
    content = request.form['data']
    print("receive:", request.form['url'])
    HtmlProcessor(content)
    return "Data received successfully!"
    # return "Data received successfully!", 200, {'Access-Control-Allow-Origin': 'https://www.baidu.com'}


if __name__ == '__main__':
    app.run(debug=True)
