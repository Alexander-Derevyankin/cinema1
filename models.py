from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from hashlib import md5
import re
from flask_security import UserMixin, RoleMixin

roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer(), db.ForeignKey("role.id")))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)

    about_me = db.Column(db.String(140))
    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))
    last_seen = str(db.Column(db.DateTime, default=datetime.utcnow))
    active = db.Column(db.Boolean())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


def slugify(s):
    pattern = r'[^\w+]'
    format_str = re.sub(pattern, '-', s).lower()
    while '--' in format_str:
        format_str = format_str.replace('--', '-')
    return format_str


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(140), unique=True)
    created = db.Column(db.DateTime, index=True, default=datetime.now())

    title = db.Column(db.String(140))
    picture = db.Column(db.Text)
    video = db.Column(db.String(300))

    premier = db.Column(db.String(140))
    producer = db.Column(db.String(140))
    inroles = db.Column(db.String(500))
    genre = db.Column(db.String(140))
    country = db.Column(db.String(140))
    duration_film = db.Column(db.String(140))
    age = db.Column(db.String(140))
    body = db.Column(db.Text)
    prewiew = db.Column(db.Text)
    soon = db.Column(db.Boolean)
    full = db.Column(db.Text)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return "<Post id: {}, title: {}>".format(self.id, self.title)



###Admin


class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)

    description = db.Column(db.String(256))
