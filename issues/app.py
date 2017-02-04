from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BASEURL = 'http://127.0.0.1:5050/issues/api'

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/project', methods=['GET'])
def project():

    r = requests.get('{}/project'.format(BASEURL))

    return render_template('project.html', project=r.json())


@app.route('/issue', methods=['GET'])
def issue():

    r = requests.get('{}/issue'.format(BASEURL))

    return render_template('issue.html', issue=r.json())

if __name__ == '__main__':
    app.run(port=5000, debug=True)
