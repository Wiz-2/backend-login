# Import necessary modules from Flask and other libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask application
app = Flask(__name__)

ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')

# Configure Cross-Origin Resource Sharing (CORS) to allow requests from the specified origin
# Adjust the 'origins' parameter as needed to match your frontend's domain
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

# In-memory user database for demonstration purposes
# In a production environment, replace this with a persistent database
users_db = {
    "testuser": generate_password_hash("password123"),  # Predefined user for testing
    "john": generate_password_hash("doe123")            # Another predefined user
}

@app.route('/api/login', methods=['POST'])
def login():
    """
    Endpoint to handle user login.
    Expects a JSON payload with 'username' and 'password'.
    Returns a success message if credentials are valid, otherwise an error message.
    """
    data = request.json  # Parse JSON data from the request body

    username = data.get('username')  # Extract 'username' from the payload
    password = data.get('password')  # Extract 'password' from the payload

    # Check if the username exists in the database
    if username in users_db:
        # Verify the provided password against the stored hashed password
        if check_password_hash(users_db[username], password):
            return jsonify({"message": "Login successful!"}), 200  # HTTP 200 OK
        else:
            # Password does not match
            return jsonify({"message": "Invalid credentials!"}), 401  # HTTP 401 Unauthorized
    else:
        # Username does not exist in the database
        return jsonify({"message": "User not found! Would you like to register?"}), 404  # HTTP 404 Not Found

@app.route('/api/register', methods=['POST'])
def register():
    """
    Endpoint to handle user registration.
    Expects a JSON payload with 'username' and 'password'.
    Returns a success message upon successful registration or an error message if the username already exists.
    """
    data = request.json  # Parse JSON data from the request body

    username = data.get('username')  # Extract 'username' from the payload
    password = data.get('password')  # Extract 'password' from the payload

    # Validate that both username and password are provided
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400  # HTTP 400 Bad Request

    # Check if the username already exists in the database
    if username in users_db:
        print("Username already exists")  # Debug statement for existing username
        return jsonify({"message": "Username already exists. Please choose a different one."}), 409  # HTTP 409 Conflict

    # Hash the password for secure storage
    hashed_password = generate_password_hash(password)
    users_db[username] = hashed_password  # Store the new user in the database
    print(f"User {username} registered successfully")  # Debug statement for successful registration

    return jsonify({"message": "Registration successful! You can now log in."}), 201  # HTTP 201 Created

# Entry point of the application
if __name__ == '__main__':
    # Run the Flask development server with debug mode enabled
    # Debug mode provides detailed error pages and auto-reloads on code changes
    app.run(debug=True)

