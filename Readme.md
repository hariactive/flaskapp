# Flask MongoDB JWT Authentication API

## Overview
This is a Flask-based web application with JWT authentication, MongoDB integration, and CRUD operations.

## Features
- User registration and login with hashed passwords.
- JWT-based authentication using cookies.
- CRUD operations for managing records.
- Supports both API (JSON) and HTML rendering.

## Setup
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd <project-directory>
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file:
   ```sh
   MONGO_URI=<your-mongodb-uri>
   JWT_SECRET_KEY=<your-secret-key>
   ```
4. Run the application:
   ```sh
   python app.py
   ```

## API Endpoints
- `POST /register` - Register a new user.
- `POST /login` - User login.
- `GET /dashboard` - Protected route requiring authentication.
- `POST /create` - Create a new record.
- `PUT /update/<record_id>` - Update a record.
- `DELETE /delete/<record_id>` - Delete a record.
- `GET /read` - Get all records.
- `GET /read/<record_id>` - Get a specific record.

## License
This project is licensed under the MIT License.

