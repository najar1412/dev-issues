from flask import Flask, jsonify, request, make_response
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import config.cred as cred
from apifunc import (
    reset_db, get_project_by_id, get_project, post_project, post_issue,
    get_issue, delete_project, delete_issue
)


app = Flask(__name__)

"""
Set up dev database, if False

sudo -u postgres psql
CREATE DATABASE issues;
CREATE USER vhrender WITH PASSWORD 'vhrender2011';
ALTER ROLE vhrender SET client_encoding TO 'utf8';
ALTER ROLE vhrender SET default_transaction_isolation TO 'read committed';
ALTER ROLE vhrender SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE issues TO vhrender;
"""

BASEURL = '/issues/api'

# Int sqlalchemy engine
engine = create_engine(
    'postgresql://{}:{}@{}:5432/issues'.format(
        cred.username, cred.password, cred.ip
    ), echo=False
)

# Init sessionmaker
Session = sessionmaker(bind=engine)

# TODO: Get the logic done for issue and project for PROTOTYPE
@app.route('{}/'.format(BASEURL), methods=['GET'])
def home():

    if request.method=='GET':

        # Init session
        # session = Session()

        welcome = {
            'Issues API': {
                'Infomation': 'Client communication api. v.01. Copyright © 2017 vhdev.',
                'Requests': {
                    'POST': [
                        '/issue', '/project', '/user', '/client', '/comment'
                    ],
                    'GET': [
                        '/issue', '/project', '/user', '/client', '/comment'
                    ],
                    'PATCH': [
                        '/issue/patch', '/project/patch', '/user/patch',
                        '/client/patch', '/comment/patch'
                    ],
                    'DELETE': [
                        '/issue/delete/<int>', '/project/delete/<int>',
                        '/user/delete/<int>', '/client/delete/<int>',
                        '/comment/delete/<int>'
                    ]
                }
            }
        }

        return make_response(
            jsonify(welcome)
        ), 200


@app.route('{}/issue'.format(BASEURL), methods=['GET', 'POST'])
def issue():
    if request.method=='POST':

        query = {}
        # query dict padder (for empty values)
        for attri in request.args.items():
            query[attri[0]] = attri[1]

        # Init session
        session = Session()

        data = query
        post_issue(session, **data)

        # TODO: IMP Posting of issues
        return make_response(
            jsonify({'POST issues': 'successful'})
        ), 200

    elif request.method=='GET':
        # Init session
        session = Session()
        issues = get_issue(session)

        if len(issues) == 0:
            return make_response(
                jsonify(
                    {
                        'GET issues': {
                            'Status': 'Successful',
                            'Message': 'No issues in table'
                        }
                    }
                )
            ), 200

        # TODO: refactor to function
        result = []
        for issue in issues:
            result.append({
                'id': issue.id,
                'name': issue.name,
                'src': issue.src,
                'issue_date': issue.issue_date,
                'issue_type': issue.issue_type,
                'issue_data': issue.issue_data
            })

        # TODO: IMP getting of project
        return make_response(
            jsonify(result)
        ), 200


@app.route('{}/issue/patch'.format(BASEURL), methods=['PATCH'])
def patch_issue():
    if request.method=='PATCH':
        # Init session
        # session = Session()

        # TODO: IMP patching issues
        return make_response(
            jsonify({'PATCH issue': 'successful'})
        ), 200


@app.route('{}/issue/delete/<id>'.format(BASEURL), methods=['DELETE'])
def delete_issue(id):
    if request.method=='DELETE':
        print(id)
        # Init session
        session = Session()

        # TODO: Deleting issues is broken? asking for one arg
        delete_issue(session, id)

        # TODO: IMP deleting issues
        return make_response(
            jsonify({'DELETE issue': 'successful'})
        ), 200


@app.route('{}/project'.format(BASEURL), methods=['GET', 'POST'])
def project():
    # TODO: If no args in request, post is still successful. fix it.
    if request.method=='POST':

        query = {}
        # query dict padder (for empty values)
        for attri in request.args.items():
            query[attri[0]] = attri[1]

        # Init session
        session = Session()
        # process args
        data = query
        project = post_project(session, **data)

        # TODO: IMP Posting of projects
        return make_response(
            jsonify({'POST project': 'successful'})
        ), 200

    elif request.method=='GET':
        # Init session
        session = Session()
        projects = get_project(session)

        if len(projects) == 0:
            return make_response(
                jsonify(
                    {
                        'GET project': {
                            'Status': 'Successful',
                            'Message': 'No projects in table'
                        }
                    }
                )
            ), 200

        # TODO: refactor to function
        result = []
        for project in projects:
            result.append({
                'id': project.id,
                'name': project.name,
                'project_code': project.project_code,
                'project_iter': project.project_iter,
                'issue_id': project.issue_id
            })

        # TODO: IMP getting of project
        return make_response(
            jsonify(result)
        ), 200


@app.route('{}/project/patch'.format(BASEURL), methods=['PATCH'])
def patch_project():
    if request.method=='PATCH':
        # Init session
        # session = Session()

        # TODO: IMP patching project
        return make_response(
            jsonify({'PATCH project': 'successful'})
        ), 200


@app.route('{}/project/delete'.format(BASEURL), methods=['DELETE'])
def delete_project():
    if request.method=='DELETE':
        # Init session
        # session = Session()

        # TODO: IMP deleting project
        return make_response(
            jsonify({'DELETE project': 'successful'})
        ), 200


# TODO: IMP the below for ALPHA
@app.route('{}/user'.format(BASEURL), methods=['GET', 'POST'])
def user():
    if request.method=='POST':
        # Init session
        # session = Session()

        # TODO: IMP Posting of users
        return make_response(
            jsonify({'POST user': 'successful'})
        ), 200

    elif request.method=='GET':
        # Init session
        # session = Session()

        # TODO: IMP getting of user
        return make_response(
            jsonify({'GET user': 'successful'})
        ), 200


@app.route('{}/user/patch'.format(BASEURL), methods=['PATCH'])
def patch_user():
    if request.method=='PATCH':
        # Init session
        # session = Session()

        # TODO: IMP patching user
        return make_response(
            jsonify({'PATCH user': 'successful'})
        ), 200


@app.route('{}/user/delete'.format(BASEURL), methods=['DELETE'])
def delete_user():
    if request.method=='DELETE':
        # Init session
        # session = Session()

        # TODO: IMP deleting user
        return make_response(
            jsonify({'DELETE user': 'successful'})
        ), 200


@app.route('{}/client'.format(BASEURL), methods=['GET', 'POST'])
def client():
    if request.method=='POST':
        # Init session
        # session = Session()

        # TODO: IMP Posting of clients
        return make_response(
            jsonify({'POST client': 'successful'})
        ), 200

    elif request.method=='GET':
        # Init session
        # session = Session()

        # TODO: IMP getting of client
        return make_response(
            jsonify({'GET client': 'successful'})
        ), 200


@app.route('{}/client/patch'.format(BASEURL), methods=['PATCH'])
def patch_client():
    if request.method=='PATCH':
        # Init session
        # session = Session()

        # TODO: IMP patching client
        return make_response(
            jsonify({'PATCH client': 'successful'})
        ), 200


@app.route('{}/client/delete'.format(BASEURL), methods=['DELETE'])
def delete_client():
    if request.method=='DELETE':
        # Init session
        # session = Session()

        # TODO: IMP deleting client
        return make_response(
            jsonify({'DELETE client': 'successful'})
        ), 200


@app.route('{}/comment'.format(BASEURL), methods=['GET', 'POST'])
def comment():
    if request.method=='POST':
        # Init session
        # session = Session()

        # TODO: IMP Posting of comment
        return make_response(
            jsonify({'POST comment': 'successful'})
        ), 200

    elif request.method=='GET':
        # Init session
        # session = Session()

        # TODO: IMP getting of comment
        return make_response(
            jsonify({'GET comment': 'successful'})
        ), 200


@app.route('{}/comment/patch'.format(BASEURL), methods=['PATCH'])
def patch_comment():
    if request.method=='PATCH':
        # Init session
        # session = Session()

        # TODO: IMP patching comment
        return make_response(
            jsonify({'PATCH comment': 'successful'})
        ), 200


@app.route('{}/comment/delete'.format(BASEURL), methods=['DELETE'])
def delete_comment():
    if request.method=='DELETE':
        # Init session
        # session = Session()

        # TODO: IMP deleting comment
        return make_response(
            jsonify({'DELETE comment': 'successful'})
        ), 200


# reset_db(engine)

if __name__ == '__main__':
    app.run(port=5050, debug=True)