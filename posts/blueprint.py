from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from models import *
from .forms import PostForm
from app import db
from flask_security import login_required


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST','GET'])
@login_required
def post_create():
    form = PostForm()
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('You have a mistake.')
        return redirect(url_for('posts.post_details', slug=post.slug))

    return render_template('posts/post_create.html', form = form)



@posts.route('/')
def post_lists():
    q =  request.args.get('q')

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page=page, per_page=2)

    return render_template('posts/posts.html', posts=posts, pages=pages)


@posts.route('/<slug>')
def post_details(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404()
    return render_template('posts/post_details.html', post = post)


@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first_or_404()
    return render_template('posts/tag_detail.html', tag = tag)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def post_update(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_details', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit.html', post=post, form=form)
