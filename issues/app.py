from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BASEURL = 'http://127.0.0.1:5050/issues/api'

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/projects', methods=['GET'])
def projects():

    r = requests.get('{}/project'.format(BASEURL))

    return render_template('projects.html', project=r.json())


@app.route('/issues', methods=['GET'])
def issues():

    r = requests.get('{}/issue'.format(BASEURL))

    return render_template('issues.html', issue=r.json())


@app.route('/project', methods=['GET'])
def get_project():
    project_id = request.args.get('id')

    r = requests.get('{}/project/{}'.format(BASEURL, project_id))

    return render_template('project.html', project=r.json())


@app.route('/issue', methods=['GET'])
def get_issue():
    issue_id = request.args.get('id')

    r = requests.get('{}/issue/{}'.format(BASEURL, issue_id))

    return render_template('issue.html', issue=r.json())


@app.route('/new_issue', methods=['POST'])
def new_issue():
    # TODO: Finish form/view
    print('fuck')
    if request.method == 'POST':
        # project_id = request.form['project_id']
        issue_type = request.form['issue_type']
        issue_src = request.form['issue_src']
        issue_content = request.form['issue_content']
        issue_attached = request.form['issue_attached']

        new_issue = {
            'project_id': 'project_id',
            'issue_type': issue_type,
            'issue_src': issue_src,
            'issue_content': issue_content,
            'issue_attached': issue_attached,
        }

        print(new_issue)

    # r = requests.get('{}/issue/{}'.format(BASEURL, issue_id))

    return render_template('issue.html')



@app.route('/query', methods=['POST'])
def query():
    # TODO: Figure out how to search multiple tables?
    if request.method == 'POST':
        query = request.form['query']
        if query.isdigit():
            # if digital search table id's.
            r = requests.get('{}/issue/{}'.format(BASEURL, query))

            if r == None:
                return render_template(
                    'query.html', query='No Issues'
                )

            return render_template(
                'query.html', query=query, issues=r.json()
            )
        else:
            pass


    return render_template('query.html', query=query)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
