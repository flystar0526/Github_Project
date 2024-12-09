import os
from flask import render_template, redirect, url_for, flash, current_app, jsonify
from flask_login import current_user, login_required
from models import db, Post, Comment, PostLike, PostFavor
from post import post_bp
from utils.forms import PostForm, CommentForm
from utils.gcs import gcs_helper

@post_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Handle image upload to GCS
        image_url = None
        if form.image.data:
            try:
                image_url = gcs_helper.upload_file(form.image.data, folder="posts")
            except Exception as e:
                flash(f'圖片上傳失敗：{str(e)}', 'danger')
                return redirect(url_for('post.create_post'))

        # Create post
        post = Post(
            title=form.title.data,
            content=form.content.data,
            image=image_url,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()

        flash('貼文已建立', 'success')
        return redirect(url_for('index'))

    return render_template('post/create_post.html', form=form)

@post_bp.route('/<post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            post_id=post_id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('留言已新增', 'success')
        return redirect(url_for('post.post_detail', post_id=post_id))

    return render_template('post/post_detail.html', post=post, form=form)

@post_bp.route('/like/<post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = PostLike.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if like:
        # If already liked, then unlike
        db.session.delete(like)
        db.session.commit()
        return jsonify({'status': 'unliked', 'likes_count': post.likes_count})
    else:
        # Add like
        new_like = PostLike(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({'status': 'liked', 'likes_count': post.likes_count})

@post_bp.route('/favor/<post_id>', methods=['POST'])
@login_required
def favor_post(post_id):
    post = Post.query.get_or_404(post_id)
    favor = PostFavor.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if favor:
        # If already favorited, then unfavorite
        db.session.delete(favor)
        db.session.commit()
        return jsonify({'status': 'unfavorited', 'favorites_count': post.favorites_count})
    else:
        # Add to favorites
        new_favor = PostFavor(user_id=current_user.id, post_id=post_id)
        db.session.add(new_favor)
        db.session.commit()
        return jsonify({'status': 'favorited', 'favorites_count': post.favorites_count})
