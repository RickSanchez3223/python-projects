from flask import flash, session
from forms.login import LoginForm
from werkzeug.security import check_password_hash

from flask import render_template, redirect, url_for
from flask import Blueprint


# Create a Blueprint instance for the 'login-out' module
login_logout = Blueprint('login-logout', __name__)


@login_logout.route("/login", methods=['GET', 'POST'], endpoint='login_view')
def login_view():
    form = LoginForm()

    if form.validate_on_submit():
        # Check the user's credentials (email/phone and password)
        email_or_phone = form.email_or_phone.data
        password = form.password.data
        query = {
            '$or': [
                    {'email': email_or_phone},
                    {'phone': email_or_phone}
                ]
            }
        from app import mongo
        user = mongo.db.user.find_one(query)
        if not user:
            print("User not found in DB")
            flash('User not found', 'error')
        elif check_password_hash(user['password'], password):
            session['email'] = user['email']
            session['role'] = user['role']
            session['permissions'] = set(mongo.db.role.find_one({'name': user['role']})['permissions'])
            flash('Login successful', 'success')
            print('Login successful', 'success')
            return redirect(url_for('user-details.user_details_view'))
        else:
            print("Wrong credentials")
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html', form=form)


@login_logout.route('/logout', endpoint='logout_view', methods=['POST'])
def logout_view():
    session.clear()
    print("Log out is Done")
    flash('Logged out', 'success')
    return redirect(url_for('login-logout.login_view'))
