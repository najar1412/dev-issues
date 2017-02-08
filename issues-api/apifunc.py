import config.cred as cred
from models import Base, Project, Issue, User, Client, Comment

# private functions
def reset_db(engine):
    """drops tables and rebuild"""
    try:
        Issue.__table__.drop(engine)
        User.__table__.drop(engine)
        Client.__table__.drop(engine)
        Comment.__table__.drop(engine)
        Project.__table__.drop(engine)
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





def get_project(session):
    """Returns all project objects"""
    projects = []
    for project in session.query(Project).order_by(Project.id):
        projects.append(project)

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
        project_iter=query['project_iter']
    )

    session.add(project)
    session.commit()

    return project


def patch_project(session, id):
    pass


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


def get_issue_by_project(session, id):
    pass


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
        group=query['group'], src=query['src'], issue_date=query['issue_date'],
        issue_type=query['issue_type'], issue_data=query['issue_data'],
    )

    append_to_project = session.query(Project).get(query['project_id'])
    append_to_project.issues.append(issue)

    session.add(issue)
    session.commit()
    session.close()

    return issue


def patch_issue(session, _id):
    pass

def delete_issue():
    pass
