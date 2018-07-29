from root import app, bcrypt, db
from flask import render_template, flash, url_for, redirect, request, abort, jsonify
from werkzeug.urls import url_parse
from root.forms import (UserRegistrationForm, UserLoginForm, RequestPassword,
                        ResetPassword, UpdateUserDetails, UploadResume,
                        UpdateUserPersonalDetails, MessageForm, ContactFrom,
                        ResumeDetails)
from root.models import User, Message, Notification, Resume
from flask_login import login_required, logout_user, login_user, current_user
from root.email import send_reset_email, send_contact_us_email
from root.functions import save_picture, save_resume
from datetime import datetime


@app.route('/')
@login_required
def home():
    print(current_user)
    r = current_user.resume_details
    edu = current_user.resume_details.filter_by(category='EDUCATION')
    pe = current_user.resume_details.filter_by(category='PROFESSIONAL EXPERIENCE')
    pw = current_user.resume_details.filter_by(category='PROJECT WORK')
    ea = current_user.resume_details.filter_by(category='EXTRACURRICULAR ACTIVITY')
    image = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('profile.html', title='Home', user=current_user,
                           image_file=image, r=r, edu=edu, pe=pe, pw=pw, ea=ea)


# user section
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # noinspection PyArgumentList
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully! now you can login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register User', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        image = url_for('static', filename='profile_pics/' + user.image)
        return render_template('profile.html', user=user, image_file=image)
    else:
        flash('User doesn\'t exists', 'info')
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # flash('Login Successful', 'success')
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user.email)
        send_reset_email(user)
        flash('An Email is send to your Email with instructions', 'success')
        return redirect('login')
    return render_template('request_password.html', title='Request Password Change',
                           form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expire token!', 'danger')
        return redirect(url_for('forget_password'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password reset successfully!!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserDetails()
    if form.validate_on_submit():
        if form.picture.data:
            picture_fn = save_picture(form.picture.data)
            current_user.image = picture_fn
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('account.html', title='Account', image_file=image, form=form)


@app.route('/upload_resume', methods=['POST', 'GET'])
@login_required
def upload_resume():
    form = UploadResume()
    if form.validate_on_submit():
        resume_fn = save_resume(form.picture.data)
        print(resume_fn)
        current_user.resume = resume_fn
        db.session.commit()
        flash('Your resume is Uploaded Successfully!!', 'success')
        return redirect(url_for('home'))
    image = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('upload_resume.html', title='Upload Resume', form=form,
                           image_file=image)


@app.route('/resume')
@login_required
def resume():
    file = url_for('static', filename='resume/' + current_user.resume)
    print(file)
    # response = make_response(url_for('static', filename='resume/' + current_user.resume))
    #
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'inline; filename={}'.format(current_user.resume)
    return redirect(file)


@app.route('/update_user_details', methods=['GET', 'POST'])
@login_required
def update_user_details():
    form = UpdateUserPersonalDetails()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.dob = form.dob.data
        current_user.mobile = form.mobile.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.country = form.country.data
        current_user.city = form.city.data
        current_user.hobbies = form.hobbies.data
        db.session.commit()
        flash('Details Updated Successfully!!', 'success')
    if request.method == 'GET':
        form.name.data = current_user.name
        form.dob.data = current_user.dob
        form.mobile.data = current_user.mobile
        form.phone.data = current_user.phone
        form.address.data = current_user.address
        form.country.data = current_user.country
        form.city.data = current_user.city
        form.hobbies.data = current_user.hobbies
    image = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('update_user_details.html', form=form, title='Update User Details',
                           image_file=image)


@app.route('/search', methods=['GET', 'POST'])
def search_user():
    print(request.form.get('username'))
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User does not exits!!', 'info')
        abort(404)
    else:
        image = url_for('static', filename='profile_pics/' + user.image)
        return render_template('profile.html', user=user, image_file=image)
    return redirect(url_for('home'))


@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    print(recipient)
    user = User.query.filter_by(username=recipient).first_or_404()
    print(user.username)
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        # db.session.commit()
        # for notification update
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('Your message has been sent', 'success')
        return redirect(url_for('user', username=recipient))
        # return redirect(url_for('home'))
    return render_template('send_message.html', title='Send Message', form=form,
                           recipient=recipient)


@app.route('/messages')
@login_required
def messages():
    # for notifications
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    # # end
    # # current_user.last_message_read_time = datetime.utcnow()
    # # db.session.commit()
    # messages = current_user.messages_received.order_by(Message.timestamp.desc())
    # return render_template('messages.html', messages=messages)
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(page, 5, False)
    next_url = url_for('messages', page=messages.next_num) if messages.has_next else None
    prev_url = url_for('messages', page=messages.prev_num) if messages.has_prev else None
    return render_template('messages.html', messages=messages.items, next_url=next_url, prev_url=prev_url)


@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@app.route('/contact_us', methods=['POST', 'GET'])
@login_required
def contact_us():
    form = ContactFrom()
    if form.validate_on_submit():
        send_contact_us_email(user=current_user, subject=form.subject.data, body=form.body.data)
        flash('Your message is send, we will contact you soon', 'info')
        return redirect(url_for('home'))
    return render_template('contact_us.html', form=form, title='Contact Us')


@app.route('/resume_details', methods=['POST', 'GET'])
@login_required
def resume_details():
    form = ResumeDetails()
    # category = request.form.get('category')
    print(form.category.data)
    if form.validate_on_submit():
        details = Resume(resume_details=current_user, category=form.category.data, year=form.year.data,
                         title=form.title.data, sub_title=form.sub_title.data, body=form.body.data)
        db.session.add(details)
        db.session.commit()
        flash('Your details saved', 'success')
        return redirect(url_for('resume_details'))

    return render_template('resume_details.html', form=form, title='Resume Details')


@app.route('/update_resume_details/<id>', methods=['POST', 'GET'])
@login_required
def update_resume_details(id):
    form = ResumeDetails()
    resume_detail = Resume.query.filter_by(id=id).first_or_404()
    print(resume_detail.resume_details.username)
    if resume_detail.resume_details.username != current_user.username:
        abort(403)
    if form.validate_on_submit():
        resume_detail.category = form.category.data
        resume_detail.year = form.year.data
        resume_detail.title = form.title.data
        resume_detail.sub_title = form.sub_title.data
        resume_detail.body = form.body.data
        db.session.commit()
        flash('Details Updated Successfully!', 'success')
    if request.method == 'GET':
        form.category.data = resume_detail.category
        form.title.data = resume_detail.title
        form.sub_title.data = resume_detail.sub_title
        form.body.data = resume_detail.body
        form.year.data = resume_detail.year
    return render_template('resume_details.html', form=form, tilte='Update details')


@app.route('/resume_details/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_resume_details(id):
    resume_detail = Resume.query.filter_by(id=id).first_or_404()
    if resume_detail.resume_details.username != current_user.username:
        abort(403)
    db.session.delete(resume_detail)
    db.session.commit()
    flash('Details deleted successfully!', 'success')
    return redirect(url_for('home'))

