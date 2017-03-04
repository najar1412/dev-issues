from .models import Base, Project, Issue, User, Client, Comment

# test setup
def __helper():
    pass

# private functions
#--
def __reset_db(session, engine):
    """DEV: drops tables and rebuild"""
    session.close()

    try:
        import sqlalchemy
        meta = sqlalchemy.MetaData(engine)
        meta.reflect()
        meta.drop_all()
    except:
        print('----------------------------')
        print('Table have not been deleted.')
        print('----------------------------')
    try:
        Base.metadata.create_all(engine)
    except:
        print('---------------------------')
        print('Tables have not been built.')
        print('---------------------------')

    print('----------------------------------------')
    print('Tables removed, and re-built successful.')
    print('----------------------------------------')

    # TODO: is return True 'pythonic', something better?
    return True


# Public functions
#--
# project functions
def get_project(session):
    """Returns all project objects"""
    projects = []
    bla = session.query(Project).all()
    for project in session.query(Project).order_by(Project.id):
        projects.append(project)

    return projects


def get_project_by_id(session, id):
    # TODO: More programmical-magic, less hardcoding.
    # TODO: Datetime formatting, (currently using slicing)
    """return project object by id"""
    project = session.query(Project).get(id)
    p_issues = [str(x) for x in project.issues]
    bla = {}
    for issue in project.issues:
        bla[issue.id] = [str(issue.issue_date)[:-10], issue.issue_complete]

    project_columns = Project.__table__.columns.keys()

    result = []
    # TODO: Make better.
    try:
        result.append(
            {
                project_columns[0]: project.id,
                project_columns[1]: project.name,
                project_columns[2]: project.project_code,
                project_columns[3]: project.project_iter,
                project_columns[4]: project.archived,
                project_columns[5]: project.client,
                'issues': bla
            }
        )

    except:
        return None

    return result


def post_project(session, **kwarg):
    """ create new project """
    # Validated query
    query = {}
    # Check user columns
    project_columns = Project.__table__.columns.keys()
    # compare user column data to database columns
    for k, v in kwarg.items():
        if k in project_columns:
            query[k] = v
        else:
            # Skip elements not in database column
            pass

    for column in project_columns:
        # if user data does include all database columns. They're added to
        # approval query variable and padded with 'None'
        if column not in kwarg and column != 'id':
            query[column] = None

    # create new project and commit to database
    project = Project(
        name=query['name'], project_code=query['project_code'],
        project_iter=query['project_iter']
    )

    session.add(project)
    session.commit()

    test = {
        'id': project.id,
        'name': project.name,
        'project_code': project.project_code,
        'project_iter': project.project_iter
    }

    session.close()

    return test


def patch_project(session, **kwarg):
    project = session.query(Project).get(kwarg['id'])
    if 'name' in kwarg:
        project.name = kwarg['name']

    elif 'issues' in kwarg:
        if isinstance(kwarg['issues'], str):

            issue = session.query(Issue).get(int(kwarg['issues']))
            project.issues.append(issue)

        elif isinstance(kwarg['issues'], list):
            # process is lit is passed
            pass

    elif 'rem-issue' in kwarg:
        if isinstance(kwarg['rem-issues'], str):

            issue = session.query(Issue).get(int(kwarg['rem-issues']))
            project.issues.remove(issue)

        elif isinstance(kwarg['rem-issues'], list):
            # process is lit is passed
            pass

    session.commit()


    # TODO: Return the patched proejct as dict/json?
    return True


def delete_project(session, _id):
    try:
        to_delete = session.query(Project).get(_id)
        if to_delete:
            session.delete(to_delete)

            session.commit()
            session.close()

            return True

        elif to_delete == None:
            return None
    except:
        # TODO: Catch proper errors
        return False


# issue functions
def get_issue(session):
    """Returns all issue objects"""
    issues = []
    for issue in session.query(Issue).order_by(Issue.id):
        issues.append(issue)
    session.close()

    return issues


def get_issue_by_id(session, id):
    issue = session.query(Issue).get(id)

    issue_columns = Issue.__table__.columns.keys()

    result = []
    # TODO: Make better.
    try:
        result.append(
            {
                issue_columns[0]: issue.id,
                issue_columns[1]: issue.group,
                issue_columns[2]: issue.src,
                issue_columns[3]: str(issue.issue_date)[:-10],
                issue_columns[4]: issue.issue_type,
                issue_columns[5]: issue.issue_data,
                issue_columns[6]: issue.issue_complete,
                issue_columns[7]: issue.project_id
            }
        )

    except:
        return None

    return result


def get_issue_by_project(session, id):
    pass


def post_issue(session, **kwarg):
    """ create new issue """
    # Validated query
    query = {}
    # Check user columns
    issue_columns = Issue.__table__.columns.keys()
    # compare user column data to database columns
    for k, v in kwarg.items():
        if k in issue_columns:
            # if match append user data to approved query variable
            query[k] = v
        else:
            # Skip elements not in database column
            pass

    for column in issue_columns:
        # if user data does include all database columns. They're added to
        # approval query variable and padded with 'None'
        if column not in kwarg and column != 'id':
            query[column] = None

    # create new collection and commit to database
    # TODO: Is there a better programmically to do the below? To remove
    # hardcodings
    issue = Issue(
        group=query['group'], src=query['src'], issue_date=query['issue_date'],
        issue_type=query['issue_type'], issue_data=query['issue_data'],
    )

    session.add(issue)

    if 'project_id' in query:
        project = session.query(Project).get(int(query['project_id']))
        project.issues.append(issue)
        session.add(project)

    session.commit()


    test = {
        'id': issue.id
    }


    return test


def patch_issue(session, **kwarg):
    issue = session.query(Issue).get(kwarg['id'])
    if 'data' in kwarg:
        issue.issue_data = kwarg['data']

    elif 'signoff' in kwarg:
        if int(issue.issue_complete) == 1:
            issue.issue_complete = 0

        else:
            issue.issue_complete = 1

    session.commit()


    # TODO: Return the patched proejct as dict/json?
    return True


def delete_issue():
    pass
