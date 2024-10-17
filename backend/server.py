from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from auth import user_auth_register, user_auth_login, user_auth_logout, user_auth_validate_token
from forum import user_create_forum, user_add_reply
from data import admin_retrieve_forum_data

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XXS and JS 
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Helps prevent CSRF attacks from different sites

CORS(app)

@app.route('/') 
def index():
    return 'Index route'

# POST API to register a user
@app.route('/auth/register', methods=['POST'])
def register_user():
    data = request.json
    email = data['email']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']

    try:
        session_token = user_auth_register(email, password, first_name, last_name)
        return jsonify({"message": "User registered successfully", "token": session_token}), 201
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 406

@app.route('/auth/login', methods=['POST'])
def login_user():
    data = request.json
    email = data['email']
    password = data['password']

    try:
        session_token = user_auth_login(email, password)
        return jsonify({"message": "User logged in successfully", "token": session_token}), 201
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

@app.route('/auth/logout', methods=['DELETE'])
def logout_user():
    data = request.json
    session_token = data['sessionToken']

    try:
        user_auth_logout(session_token)
        return jsonify({"message": "User logged out successfully"}), 200
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

    
@app.route('/forum/new/question', methods=['POST']) 
def create_new_forum():
    data = request.json
    forum_title = data['title']
    forum_question = data['forumQuestion']
    session_token = data['sessionToken']

    try:
        user_create_forum(forum_title, forum_question, session_token)
        return jsonify({"message": "Forum created succesfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
@app.route('/forum/retrieve', methods=['GET']) 
def retrieve_all_forums():
    try:
        forum_dict = admin_retrieve_forum_data()
        return jsonify({"message": "All forum data returned succesfully", "forums": forum_dict}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/auth/validate', methods=['POST'])
def validate_token():
    data = request.json
    session_token = data['sessionToken']

    try:
        if (user_auth_validate_token(session_token)):
                return jsonify({"message": "Token is valid"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/forum/reply/submit', methods=['POST'])
def store_reply():
    data = request.json
    forum_id = data['forumId']
    reply_comment = data['reply']
    session_token = data['sessionToken']

    try:
        user_add_reply(forum_id, reply_comment, session_token)
        return jsonify({"message": "Forum reply added succesfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5005)