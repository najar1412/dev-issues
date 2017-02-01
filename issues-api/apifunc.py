import config.cred as cred
from models import Base, Project, Issue, User, Client, Comment

# private functions
def reset_db(engine):
    """drops tables and rebuild"""
    try:
        Project.__table__.drop(engine)
        Issue.__table__.drop(engine)
        User.__table__.drop(engine)
        Client.__table__.drop(engine)
        Comment.__table__.drop(engine)
        print('Old tables removed')
    except:
        print('failed to remove old tables')
    try:
        Base.metadata.create_all(engine)
        print('new tables built')
    except:
        print('failed to build new tables.')

    return True


# Public functions
def get_project_by_id(session, id):
    # TODO: More programmical-magic, less hardcoding.
    """return project object by id"""
    project_by_id = session.query(Project).get(id)

    project_columns = Project.__table__.columns.keys()

    """
    result = {
        'id': patron_by_id.id, 'client': patron_by_id.client,
        'contact': patron_by_id.contact, 'contactphone': patron_by_id.contactphone,
        'contactemail': patron_by_id.contactemail, 'user': {}
    }

    for i in patron_by_id.user:
        result['user'][i.id] = {
            'name': i.name, 'team': i.team
        }

    return result
    """
    return None


def get_project(session):
    """Returns all project objects"""
    projects = []
    for project in session.query(Project).order_by(Project.id):
        projects.append(project)
    session.close()

    for x in projects:
        print(x)

    return projects


def post_project(session, **kwarg):
    """ create new project """
    # Validated query
    query = {}
    # Check user columns
    project_columns = Project.__table__.columns.keys()
    # compare user column data to database columns
    for k, v in kwarg.items():
        if k in project_columns:
            # if match append user data to approved query variable
            query[k] = v
        else:
            # Skip elements not in database column
            pass

    for column in project_columns:
        # if user data does include all database columns. They're added to
        # approval query variable and padded with 'None'
        if column not in kwarg and column != 'id':
            query[column] = None

    # create new collection and commit to database
    project = Project(
        name=query['name'], project_code=query['project_code'],
        project_iter=query['project_iter'], issue_id=query['issue_id']
    )

    session.add(project)
    session.commit()
    session.close()

    return project


def patch_project(session, id):
    pass


def delete_project(session, id):
    try:
        to_delete = session.query(Project).get(id)
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


def get_issue_by_project(session, id):
    pass


def get_issue_by_id(session, id):
    pass

def get_issue(session):
    """Returns all issue objects"""
    issues = []
    for issue in session.query(Issue).order_by(Issue.id):
        issues.append(issue)
    session.close()

    return issues


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
        name=query['name'], src=query['src'], issue_date=query['issue_date'],
        issue_type=query['issue_type'], issue_data=query['issue_data']
    )

    session.add(issue)
    session.commit()
    session.close()

    return issue


def patch_issue(session, id):
    pass


def delete_issue(session, id):
    try:
        to_delete = session.query(Issue).get(id)
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
