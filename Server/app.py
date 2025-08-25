from flask import Flask
from flask_cors import CORS
from models.user_model import User
from routes.user_routes import user_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/users')

# Create database tables
User.create_table()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)

