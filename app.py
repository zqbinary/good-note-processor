from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS

from service.HtmlProcessor import HtmlProcessor
from service.TableProcessor import TableProcessor

app = Flask(__name__)
CORS(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    return redirect(url_for('out'))


@app.route('/tt')
def tt():
    return 't5'


@app.route('/test/<param>')
def test_show(param):
    return render_template(f'/tests/{param}/out.html')


@app.route('/table')
def out_html():
    processor = TableProcessor('file')
    processor.do()
    content = processor.read_table_file()
    return content


@app.route('/out')
def out():
    processor = TableProcessor('file')
    content = processor.read_out_file()
    return content


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
    app.run()
