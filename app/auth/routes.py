from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify, current_app
from firebase_admin import auth

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    current_app.logger.info("Signup attempt - currently disabled")
    return jsonify({'error': 'Signup is currently disabled.'}), 403

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_token = request.form.get('idToken')
        if not id_token:
            current_app.logger.warning("Login attempt without ID token")
            return render_template('login.html', error="Missing ID token.")
            
        try:
            decoded_token = auth.verify_id_token(id_token)
            session['user_id'] = decoded_token['uid']
            session['email'] = decoded_token.get('email')
            session.permanent = True
            
            current_app.logger.info(f"User logged in successfully: {session.get('email', 'Unknown')}")
            return redirect(url_for('main.home'))
            
        except Exception as e:
            current_app.logger.warning(f"Login failed: {str(e)}")
            return render_template('login.html', error=f"Invalid token: {str(e)}")
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    user_email = session.get('email', 'Unknown')
    session.clear()
    current_app.logger.info(f"User logged out: {user_email}")
    return redirect(url_for('auth.login'))

@auth_bp.route('/sessionLogin', methods=['POST'])
def session_login():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        id_token = data.get('idToken')

        if not id_token:
            current_app.logger.warning("Session login attempt without ID token")
            return jsonify({'error': 'ID token missing'}), 400

        decoded_token = auth.verify_id_token(id_token)
        session['user_id'] = decoded_token['uid']
        session['email'] = decoded_token.get('email')
        session.permanent = True
        
        current_app.logger.info(f"Session login successful: {session.get('email', 'Unknown')}")
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        current_app.logger.warning(f"Session login failed: {str(e)}")
        return jsonify({'error': f'Invalid token: {str(e)}'}), 401