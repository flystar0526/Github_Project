import os
import uuid
from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from models import db, Post
from post import post_bp
from utils.forms import PostForm

UPLOAD_FOLDER = 'static/posts'

@post_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Image upload handling
        image_filename = None
        if form.image.data:
            image_file = form.image.data
            original_filename = secure_filename(image_file.filename)
            # Use UUID to generate a unique file name, retaining the extension
            unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(original_filename)[1]}"
            image_path = os.path.join(current_app.root_path, UPLOAD_FOLDER, unique_filename)

            # Ensure the upload folder exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            # Save the image
            image_file.save(image_path)
            image_filename = unique_filename

        # Create post
        post = Post(
            title=form.title.data,
            content=form.content.data,
            image=image_filename,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()

        flash('貼文已建立', 'success')
        return redirect(url_for('index'))

    return render_template('post/create_post.html', form=form)