from flask import Blueprint
from flask import render_template
from .forms import PostForm
from app.models import Post
from flask import request, redirect, url_for
from app import db
from flask_security import login_required

posts = Blueprint("posts", __name__, template_folder="templates")


# http://localhost/blog/create
@login_required
@posts.route("/create", methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form['body']
        if title:
            try:
                post = Post(title=title, body=body)
                db.session.add(post)
                db.session.commit()
            except:
                print("Something wrong")
            return redirect(url_for("posts.index"))
    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@login_required
@posts.route("/<slug>/edit", methods=["POST", "GET"])
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first()

    if request.method == "POST":
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for("posts.post_detail", slug=post.slug))

    form = PostForm(obj=post)
    return render_template("posts/edit_post.html", post=post, form=form)


@posts.route("/film")
def index():
    q = request.args.get("q")
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:
        posts = Post.query.order_by(Post.created.desc())
    return render_template("posts/index.html", posts=posts)


@posts.route("/soon")
def soon():
    q = request.args.get("q")
    if q:
        postsoon = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:
        postsoon = Post.query.order_by(Post.created.desc())
    return render_template("posts/soon.html", postsoon=postsoon)


@posts.route("/<slug>")
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template("posts/post_detail.html", post=post)
