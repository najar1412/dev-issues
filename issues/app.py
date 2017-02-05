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


@app.route('/query', methods=['POST'])
def query():
    # TODO: Figure out how to search multiple tables?
    if request.method == 'POST':
        query = request.form['query']
        if query.isdigit():
            # if digital search table id's.
            r = requests.get('{}/issue/{}'.format(BASEURL, query))
            return render_template(
                'query.html', query=query, issue=r.json()
            )
        else:
            pass


    return render_template('query.html', query=query)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
