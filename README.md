# Expense Tracker API

## Description
This is a Flask backend API that allows users to sign up, log in, and manage their personal expenses. Each user can only access and modify their own data.

## Features
- User authentication (signup, login, logout, session check)
- Secure password hashing using bcrypt
- Full CRUD for expenses
- Pagination for viewing expenses
- Protected routes (users can only access their own expenses)

## Installation
```bash
pipenv install
pipenv shell
```

## Database Setup
```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

## Seed Database
```bash
python seed.py
```

## Run the App
```bash
flask run
```

## API Endpoints

### Auth
- POST /signup  
- POST /login  
- DELETE /logout  
- GET /me  

### Expenses
- POST /expenses  
- GET /expenses?page=1&per_page=5  
- GET /expenses/<id>  
- PATCH /expenses/<id>  
- DELETE /expenses/<id>  