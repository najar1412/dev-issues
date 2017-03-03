from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# TODO: Project needs a 'location' field? to sort by location.
# TODO: Issues needs to be in 'states'. 'new', 'review/commence', 'complete'?
# a simple way of tracking process
Base = declarative_base()

class Project(Base):
    # TODO: IMP start date, deadlines etc.
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    project_code = Column(String)
    project_iter = Column(Integer)
    archived = Column(Integer, default=0)
    client = Column(String, default='test')
    # relational data
    issues = relationship(
        "Issue", backref='project'
    )

    def __repr__(self):
        return "<Project(id='%s', name='%s', client'%s'>" % (
            self.id, self.name, self.client
        )


class Issue(Base):
    __tablename__ = 'issue'

    id = Column(Integer, primary_key=True)
    group = Column(String)
    src = Column(String)
    issue_date = Column(DateTime, default=func.now())
    issue_type = Column(String)
    issue_data = Column(String)
    issue_complete = Column(Integer, default=0)

    # relational data
    project_id = Column(Integer, ForeignKey('project.id'))

    def __repr__(self):
        return "<Issue(id='%s', group='%s')>" % (
            self.id, self.group
        )


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (
            self.id, self.name
        )


class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Client(id='%s', name='%s')>" % (
            self.id, self.name
        )


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    parent_comment = Column(Integer)
    comment = Column(String)

    def __repr__(self):
        return "<Comment(id='%s', parent_comment='%s')>" % (
            self.id, self.parent_comment
        )
