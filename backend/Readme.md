
# Recipe Management System - Backend

This directory contains the backend for the Recipe Management System, a multi-tenant RESTful API built with Python and Django REST Framework.

## Project Overview

The goal of this project is to provide a simple, robust API for managing kitchen recipes. It's designed to be used by multiple, potentially competing, restaurants, ensuring that each restaurant's data (recipes, users) is kept separate.

### Core Features
- **Recipe Management**: Full CRUD (Create, Read, Update, Delete) functionality for recipes.
- **Multi-tenancy**: Data is partitioned by `Restaurant`. A user can only access recipes belonging to their own restaurant.
- **Authentication**: Uses JSON Web Tokens (JWT) for secure, stateless authentication.
- **Kitchen-Focused Design**: The API provides detailed recipe views suitable for a kitchen environment.

---
## Technology Stack

- **Framework**: Django & Django REST Framework
- **Language**: Python
- **Database**: SQLite3 (for development), PostgreSQL (recommended for production)
- **Authentication**: Simple JWT (djangorestframework-simplejwt)
- **Testing**: Django's built-in test framework

---
## Setup and Installation

Follow these steps to get the backend running on your local machine.

### 1. Prerequisites
- Python 3.8+
- `pip` package manager

### 2. Clone the Repository
If you haven't already, clone the project to your local machine.

```bash
git clone <your-repository-url>
cd recipe-management-system/backend
```
### 3. Set Up a Virtual Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```
### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Running the Application

#### 1. Apply Database Migrations
```bash
# Creates the migration files based on model changes
python manage.py makemigrations recipes

# Applies the migrations to the database
python manage.py migrate
```
#### 2. Create a Superuser
```bash
python manage.py createsuperuser
```

#### 3. Add data with management command
```bash
python manage.py seed_data
```

#### 4. Run the Development Server
```bash
python manage.py runserver
```

#### 5. Running Test
```bash
python manage.py test recipes
```

## API Endpoints

All endpoints are prefixed with `/api/`. Authentication is required for all recipe endpoints.

| Method      | Endpoint           | Description                                 |
|-------------|--------------------|---------------------------------------------|
| POST        | /token/            | Obtain a JWT access token.                  |
| POST        | /token/refresh/    | Refresh an expired JWT access token.        |
| GET         | /recipes/          | List all recipes for the user's restaurant. |
| POST        | /recipes/          | Create a new recipe.                        |
| GET         | /recipes/{id}/     | Retrieve a specific recipe.                 |
| PUT/PATCH   | /recipes/{id}/     | Update a specific recipe.                   |
| DELETE      | /recipes/{id}/     | Delete a specific recipe.                   |