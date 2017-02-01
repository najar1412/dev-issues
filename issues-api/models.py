from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    project_code = Column(String)
    project_iter = Column(Integer)

    issue_id = Column(Integer, ForeignKey('issue.id'))
    # relational data
    issue = relationship(
        "Issue", back_populates="project", single_parent=True,
        cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return "<Project(id='%s', name='%s'" % (
            self.id, self.name
        )


class Issue(Base):
    __tablename__ = 'issue'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    src = Column(String)
    issue_date = Column(Date)
    issue_type = Column(String)
    issue_data = Column(String)

    # relational data
    project = relationship(
        "Project", back_populates='issue',
        cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return "<Issue(id='%s', name='%s')>" % (
            self.id, self.name
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
