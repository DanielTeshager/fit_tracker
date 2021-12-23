# Fit Tracker - A simple fitness tracker API

## Getting Started

## Install Dependencies

Run `pip install -r requirements.txt` to install any dependencies.


## Testing the Application
1. Create a database called test_fit_tracker.
2. make sure the environmetal variables are set correctly.
3. Run the tests.

## Deployment Information
The API is deployed on Heroku.
To access the API, go to the following link: https://fittracker2.herokuapp.com/


## Role based access control
RBAC is used to control access to the API.
Auth0 is used to authenticate users and manage access.
JWT access tokens for both Admin & Gym-Attendant roles are saved in JWT tokens file.
The following roles are available:
1. Admin: Can access all endpoints.
- Can create, update, and delete users and body_measurements.
2. Gym Attendant: Can access 
- Can read body_measurements and users-details.

## Roles and Permissions

- Admin Permissions:
    - "get:user-detail",
    - "get:body_measurements",
    - "delete:body_measurements",
    - "patch:body_measurements",
    - "post:users",
    - "post:body_measurements",
    - "delete:users"
- Gym Attendant Permissions:
    - "get:user-detail",
    - "get:body_measurements"

## API Endpoints
- Thorough documentation of all the endpoints is provided in the application itself.

## Accessing the API
- The API is accessed via the following link: https://fittracker2.herokuapp.com/
- After logging in, the API will return a JWT token.
- The token is used to access the API.

# Database
sample database is created in the following location:
[]: # Path: sqfile.sql



