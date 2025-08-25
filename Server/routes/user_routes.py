from flask import Blueprint
from controllers.user_controller import UserController

# Create blueprint for user routes
user_bp = Blueprint('users', __name__)

# User registration route
@user_bp.route('/register', methods=['POST'])
def register_user():
    """
    POST /users/register
    Register a new user
    """
    return UserController.register_user()

# User login route
@user_bp.route('/login', methods=['POST'])
def login_user():
    """
    POST /users/login
    Authenticate user login
    """
    return UserController.login_user()

# Get all users route
@user_bp.route('/', methods=['GET'])
def get_all_users():
    """
    GET /users/
    Get all users
    """
    return UserController.get_all_users()

# Get user by ID route
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    GET /users/<user_id>
    Get user by ID
    """
    return UserController.get_user_by_id(user_id)

# Update user route
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    PUT /users/<user_id>
    Update user information
    """
    return UserController.update_user(user_id)

# Change password route
@user_bp.route('/<int:user_id>/change-password', methods=['PUT'])
def change_password(user_id):
    """
    PUT /users/<user_id>/change-password
    Change user password
    """
    return UserController.change_password(user_id)

# Delete user route
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    DELETE /users/<user_id>
    Delete user by ID
    """
    return UserController.delete_user(user_id)

