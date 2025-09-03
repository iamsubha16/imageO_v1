from functools import wraps
from flask import session, redirect, url_for, request, current_app

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            current_app.logger.warning(
                f"Unauthorized access attempt to {request.endpoint} from {request.remote_addr}"
            )
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function