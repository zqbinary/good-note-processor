from datetime import timedelta

from flask import Flask, render_template, request
from flask_cors import CORS

from service.HtmlProcessor import HtmlProcessor

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('out.html')


@app.route('/test/<param>')
def test_show(param):
    return render_template(f'./tests/{param}/out.html')


@app.route('/out')
def index2():
    return render_template('out.html')


@app.route('/html', methods=['POST'])
def html():
    content = request.form['data']
    HtmlProcessor.dump_location_from_str(request.form['location'])
    processor = HtmlProcessor('html', content)
    processor.do()
    return "Data received successfully!"


@app.after_request
def add_header(response):
    if 'text/css' in response.headers['Content-Type']:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Expires'] = '0'
        response.headers['Pragma'] = 'no-cache'
    return response


if __name__ == '__main__':
    app.run(debug=True, port=7826)
