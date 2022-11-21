from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()
marshmallow = Marshmallow()


class Member(db.Model):
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True,
                         primary_key=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    nationality = db.Column(db.String(80), nullable=False)
    member_since = db.Column(db.DateTime, nullable=False)
    member_uuid = db.Column(db.String(200), nullable=False)
    active = db.Column(db.String(200), nullable=False)

    def __init__(self, name, lastname, username, password, age, gender, nationality, member_since, member_uuid, active=True):
        self.member_uuid = member_uuid
        self.username = username
        self.password = password
        self.name = name
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.nationality = nationality
        self.member_since = member_since
        self.active = active
    
    def __str__(self):
        return 'Member "{}"'.format(self.username)

    def get_id(self):
        return str(self.username)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


class MemberSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('username', 'name', 'lastname', 'age','gender', 'nationality', 'member_since', 'active')
