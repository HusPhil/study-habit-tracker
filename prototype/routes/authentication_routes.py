from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models.player.player_manager import PlayerManager
from models.player.player import Player
from models.user.user_manager import UserManager
from models.database.db import db, DatabaseError
from models.user.user import User

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    # Check if the user is already logged in
    # if 'user_id' in session:
    #     return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            # Find user by username
            result = db.execute("SELECT * FROM users WHERE username = ?", (username,))
            if result:
                user = User(
                    user_id=result[0]['user_id'],
                    email=result[0]['email'],
                    username=result[0]['username'],
                    password=result[0]['password']
                )
                
                if user.login(password):
                    return redirect(url_for('index'))
            
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        except DatabaseError as e:
            flash('An error occurred. Please try again.')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required')
            return redirect(url_for('auth.register'))
            
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('auth.register'))
        
            
        try:
            # Check if username or email already exists
            result = db.execute("SELECT * FROM users WHERE username = ? OR email = ?", 
                              (username, email))
            if result:
                flash('Username or email already exists')
                return redirect(url_for('auth.register'))
            
            # Create new player
            newPlayer_data = PlayerManager.create(email, username, password)
            player = Player(**newPlayer_data)
            if player:
                player.login(password=password)
                flash('Registration successful!')
                return redirect(url_for('index'))
            
            flash('Error creating account')
            return redirect(url_for('auth.register'))
            
        except DatabaseError as e:
            flash('An error occurred. Please try again.')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

@auth_routes.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    
    user_data = UserManager.get(data['user_id'])
    print(user_data)
    user = User(**user_data)
    user.logout()

    flash("You have been logged out")

    return jsonify({"message": "You have been logged out"})  # ✅ Return as JSON
  # ✅ Redirect to login page
