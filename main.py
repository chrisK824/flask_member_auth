import json
import time
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import os
import uuid
import eventlet
from eventlet import wsgi
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from schemas.members import db, marshmallow, Member, MemberSchema

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "members.db"))
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret_key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
marshmallow.init_app(app)
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(username):
    return Member.query.filter_by(
        username=username).first()


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", member=current_user)


@app.route('/members', methods=['GET'])
@login_required
def getUsers():
    members = Member.query.all()
    return jsonify(members_schema.dump(members))


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        existing_member = Member.query.filter_by(
            username=request.form['username'], password=request.form['password']).first()
        if not existing_member:
            return jsonify({"message": "Invalid username or password!"})
        login_user(existing_member)
    return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        member = Member(name=request.form['name'],
                        lastname=request.form['lastname'],
                        username=request.form['username'],
                        password=request.form['password'],
                        age=request.form['age'],
                        gender=request.form['gender'],
                        nationality=request.form['nationality'],
                        member_since=datetime.now(),
                        member_uuid=str(uuid.uuid4()))

        existing_user = Member.query.filter_by(
            username=member.username).first()
        if not existing_user:
            db.session.add(member)
            db.session.commit()
        else:
            return jsonify({"message": "Username already used, please pick another one"}), 403

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = os.urandom(1)
    wsgi.server(eventlet.listen(('0.0.0.0', 9999)), app)
    # app.run(debug=True)
