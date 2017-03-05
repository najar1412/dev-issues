from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BASEURL = 'http://127.0.0.1:5050/issues/api'

"""
@app.route('/', methods=['GET'])
def index():
    # TODO: Figure out more elgant way to return if no projects exist.
    r = requests.get('{}/project'.format(BASEURL))
    projects = {}
    for project in r.json():
        try:
            projects[project['id']] = '{}-{} | {}'.format(
                project['project_code'], project['project_iter'], project['name']
            )
        except:
            if r.json()['GET project']['Message'] == 'No projects in table':
                return render_template('home.html', projects='false')

    return render_template('home.html', projects=projects)

"""

@app.route('/projects', methods=['GET'])
def projects():

    r = requests.get('{}/project'.format(BASEURL))
    try:
        if r.json()['GET project']['Message'] == 'No projects in table':
            return render_template('projects.html', projects='false')
    except TypeError:
        pass

    return render_template('projects.html', project=r.json())


@app.route('/', methods=['GET'])
def issues():

    projects = {}
    issue = 'false'

    # Build project list
    p = requests.get('{}/project'.format(BASEURL))

    for project in p.json():
        try:
            projects[project['id']] = '{}-{} | {}'.format(
                project['project_code'], project['project_iter'], project['name']
            )
        except:
            if p.json()['GET project']['Message'] == 'No projects in table':
                return render_template('home.html', projects='false')

    # Get issues
    r = requests.get('{}/issue'.format(BASEURL))
    try:
        issue = r.json()
        return render_template('issues.html', issue=issue, projects=projects)
    except:
        if r.json()['GET issues']['Message'] == 'No issues in table':
            issue = 'false'

    return render_template('issues.html', issue=issue, projects=projects)


@app.route('/project', methods=['GET'])
def get_project():
    project_id = request.args.get('id')

    r = requests.get('{}/project/{}'.format(BASEURL, project_id))

    return render_template('project.html', project=r.json())


@app.route('/patch_issue', methods=['GET', 'POST'])
def patch_issue():
    issue_id = request.args.get('id')
    data = {}
    # build dict of user data
    for arg in request.args:
        data[arg] = request.args[arg]

    print(data)

    g = requests.patch('{}/issue/patch?id={}&signoff={}'.format(BASEURL, data['id'], data['signoff']))

    #

    r = requests.get('{}/issue/{}'.format(BASEURL, int(data['id'])))

    return render_template('issue.html', issue=r.json())


@app.route('/issue', methods=['GET'])
def get_issue():
    issue_id = request.args.get('id')

    r = requests.get('{}/issue/{}'.format(BASEURL, issue_id))

    return render_template('issue.html', issue=r.json())


@app.route('/new_issue', methods=['POST'])
def new_issue():
    # TODO: Finish form/view
    # TODO: Figure how to access the response object From the api (race condition)
    if request.method == 'POST':
        project_id = request.form['project_id']
        issue_type = request.form['issue_type']
        issue_src = request.form['issue_src']
        issue_data = request.form['issue_data']
        issue_attached = request.form['issue_attached']

        issue = {
            'project_id': int(project_id),
            'issue_type': issue_type,
            'issue_src': issue_src,
            'issue_data': issue_data,
            'issue_attached': issue_attached,
        }

    r = requests.post(
        '{}/issue?project_id={}&issue_type={}&issue_src={}&issue_data={}&issue_attached={}'.format(
            BASEURL, issue['project_id'], issue['issue_type'],
            issue['issue_src'], issue['issue_data'], issue['issue_attached']
        )
    )

    # get newly posted project
    # TODO: remove second request. Instead have api serve all information
    # of new post.
    issue_id = r.json()['id']

    g = requests.get('{}/issue/{}'.format(BASEURL, issue_id))

    return render_template('issue.html', issue=g.json())


@app.route('/new_project', methods=['POST'])
def new_project():
    # TODO: Finish form/view
    # TODO: Figure how to access the response object From the api (race condition)
    if request.method == 'POST':

        name = request.form['name']
        project_code = request.form['project_code']
        project_iter = request.form['project_iter']

        params = {
            'name': name,
            'project_code': project_code,
            'project_iter': project_iter,
        }

        # Post new project
        r = requests.post(
            '{}/project'.format(BASEURL), params=params
        )

        # get newly posted project
        # TODO: remove second request. Instead have api serve all information
        # of new post.
        project_id = r.json()['id']

        g = requests.get('{}/project/{}'.format(BASEURL, project_id))

        return render_template('project.html', project=g.json())


@app.route('/query', methods=['POST'])
def query():
    # TODO: Figure out how to search multiple tables?
    # TODO: return page is nothing exists.
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

# Seconary wants
@app.route('/user', methods=['GET'])
def get_user():
    return render_template('user.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
