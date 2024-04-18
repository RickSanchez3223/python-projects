from flask import session, flash, redirect, url_for


# Custom decorator for session authentication and role-based access control

"""
Checks:
1. user in Session?
2. User in DB?
3. View Permission
"""


def session_authentication(permissions_required=None):
    def decorator(view_function):
        def wrapper(*args, **kwargs):
            email = session.get('email')
            if email:
                from app import mongo
                user = mongo.db.user.find_one({'email': email, 'is_deleted': False})
                if not user:
                    print("This user is not found in DB/deleted")
                    flash('You do not have permission to access the requested page.', 'error')
                    return redirect(url_for('login-logout.login_view'))
                elif permissions_required:
                    session['role'] = user['role']
                    session['permissions'] = set(mongo.db.role.find_one({'name': user['role']})['permissions'])
                    print("session details: ", session)
                    permissions = session['permissions']
                    if not set(permissions_required).isdisjoint(permissions):
                        print('Permission check passed')
                        return view_function(*args, **kwargs)
                    else:
                        print('Permission check failed')
                        flash('You do not have permission to access the requested page', 'error')
                        return redirect(url_for('user-details.user_details_view'))
                else:
                    session['role'] = user['role']
                    session['permissions'] = set(mongo.db.role.find_one({'name': user['role']})['permissions'])
                    print("session details: ", session)
                    print("This page has no permission set")
                    return view_function(*args, **kwargs)
            print("This email is not in Session")
            flash('Please log in to access this view.', 'error')
            return redirect(url_for('login-logout.login_view'))
        return wrapper
    return decorator
