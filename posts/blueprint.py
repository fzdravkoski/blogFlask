from flask import Blueprint
from flask import render_template
from flask import request
from models import *
from .forms import PostForm
posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/create')
def post_create():
    form = PostForm()
    return render_template('posts/post_create.html', form = form)



@posts.route('/')
def post_lists():
    q =  request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.all()

    return render_template('posts/posts.html', posts=posts)


@posts.route('/<slug>')
def post_details(slug):
    post = Post.query.filter(Post.slug==slug).first()
    return render_template('posts/post_details.html', post = post)


@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    return render_template('posts/tag_detail.html', tag = tag)