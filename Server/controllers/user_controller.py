from flask import jsonify, request
from models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

class UserController:
    
    @staticmethod
    def register_user():
        """
        Register a new user
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'password', 'role_id']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'error': f'Field {field} is required'}), 400
            
            # Check if user with this email already exists
            existing_user = User.get_user_by_email(data['email'])
            if existing_user:
                return jsonify({'error': 'User with this email already exists'}), 409
            
            # Hash the password before storing
            hashed_password = generate_password_hash(data['password'])
            
            # Create new user
            user_id = User.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=hashed_password,
                role_id=data['role_id']
            )
            
            if user_id:
                return jsonify({
                    'message': 'User created successfully',
                    'user_id': user_id
                }), 201
            else:
                return jsonify({'error': 'Failed to create user'}), 500
                
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    @staticmethod
    def login_user():
        """
        Authenticate user login
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            if 'email' not in data or 'password' not in data:
                return jsonify({'error': 'Email and password are required'}), 400
            
            # Get user by email
            user = User.get_user_by_email(data['email'])
            if not user:
                return jsonify({'error': 'Invalid email or password'}), 401
            
            # Check password
            if check_password_hash(user['password'], data['password']):
                # Password is correct, return user info (without password)
                user_info = {
                    'user_id': user['user_id'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'email': user['email'],
                    'role_id': user['role_id']
                }
                return jsonify({
                    'message': 'Login successful',
                    'user': user_info
                }), 200
            else:
                return jsonify({'error': 'Invalid email or password'}), 401
                
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
    @staticmethod
    def get_all_users():
        """
        Get all users from database
        """
        try:
            users = User.get_all_users()
            # Remove passwords from response for security
            for user in users:
                user.pop('password', None)
            return jsonify({'users': users}), 200
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        """
        try:
            user = User.get_user_by_id(user_id)
            if user:
                # Remove password from response for security
                user.pop('password', None)
                return jsonify({'user': user}), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
    @staticmethod
    def update_user(user_id):
        """
        Update user information
        """
        try:
            data = request.get_json()
            
            # Check if user exists
            existing_user = User.get_user_by_id(user_id)
            if not existing_user:
                return jsonify({'error': 'User not found'}), 404
            
            # Update user
            success = User.update_user(
                user_id=user_id,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                role_id=data.get('role_id')
            )
            
            if success:
                return jsonify({'message': 'User updated successfully'}), 200
            else:
                return jsonify({'error': 'Failed to update user'}), 500
                
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    @staticmethod
    def change_password(user_id):
        """
        Change user password
        """
        try:
            data = request.get_json()
            
            # Validate required fields
            if 'current_password' not in data or 'new_password' not in data:
                return jsonify({'error': 'Current password and new password are required'}), 400
            
            # Get user
            user = User.get_user_by_id(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Verify current password
            if not check_password_hash(user['password'], data['current_password']):
                return jsonify({'error': 'Current password is incorrect'}), 401
            
            # Hash new password
            new_hashed_password = generate_password_hash(data['new_password'])
            
            # Update password in database
            success = User.update_user_password(user_id, new_hashed_password)
            
            if success:
                return jsonify({'message': 'Password changed successfully'}), 200
            else:
                return jsonify({'error': 'Failed to change password'}), 500
                
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
    @staticmethod
    def delete_user(user_id):
        """
        Delete user by ID
        """
        try:
            # Check if user exists
            existing_user = User.get_user_by_id(user_id)
            if not existing_user:
                return jsonify({'error': 'User not found'}), 404
            
            # Delete user
            success = User.delete_user(user_id)
            
            if success:
                return jsonify({'message': 'User deleted successfully'}), 200
            else:
                return jsonify({'error': 'Failed to delete user'}), 500
                
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500
