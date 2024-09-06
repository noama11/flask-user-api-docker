# Flask Application with PostgreSQL and Docker

This project is a **Flask-based web application** with a **PostgreSQL** backend. It provides a basic CRUD API to manage users and utilizes **Flask-Migrate** to handle database migrations. The project is containerized using **Docker** and managed with **Docker Compose** for easier setup and management.

---

### Tools Overview

1. **Flask**: A lightweight web framework for building APIs.
2. **PostgreSQL**: A powerful relational database system used for storing user data.
3. **Flask-SQLAlchemy**: SQL toolkit for Flask, which simplifies interaction with the PostgreSQL database.
4. **Flask-Migrate**: Handles database migrations, allowing you to apply changes to the database schema over time.
5. **Docker**: Containerizes the entire application, making it easy to deploy and run consistently across different environments.
6. **Docker Compose**: Orchestrates the Flask and PostgreSQL services, ensuring they work together seamlessly.

---

## Prerequisites

Before starting, ensure you have the following installed on your machine:

- [**Docker**](https://docs.docker.com/get-docker/) (for containerization)
- [**Docker Compose**](https://docs.docker.com/compose/install/) (for multi-container orchestration)

---

## Setup Instructions

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Initialize the Migration System (First-Time Setup)

If you're setting up this project for the first time, you need to manually initialize the database migration system. This step is required only once.

Run the following command to create the `migrations/` folder in your project:

```bash
docker-compose run flaskapp flask db init
```

This command initializes the migration system and sets up Alembic to track database schema changes.

### 3. Generate and Apply Migrations

The following steps need to be run anytime you make changes to your models:

1. **Generate migration scripts**:

   ```bash
   docker-compose run flaskapp flask db migrate -m "Create users table"
   ```

2. **Apply migrations to the database**:
   ```bash
   docker-compose run flaskapp flask db upgrade
   ```

These commands ensure that any changes made to the database models are reflected in the database.

### 4. Build and Run the Application

After initializing the migrations, build and run the application using Docker Compose:

```bash
docker-compose up --build
```

This command will:

- Build the Flask application image.
- Run the PostgreSQL database container.
- Apply any migrations.
- Start the Flask app on port 4000.

Once running, you can access the application at:

- **http://localhost:4000**

### 4. API Endpoints

The following API endpoints are available:

- **GET** `/test`: A test route to ensure the API is running. Returns a simple message.
- **GET** `/api/users`: Retrieve all users.
- **GET** `/api/users/<user_id>`: Retrieve a specific user by their ID.
- **POST** `/api/users`: Create a new user. The request body should include a JSON with a `username` field.

#### Example Request for Creating a User:

To create a new user, use the following `curl` command or any API testing tool:

```bash
curl -X POST http://localhost:4000/api/users -H "Content-Type: application/json" -d '{"username": "new_user"}'
```

---

## Database Migrations

This project uses **Flask-Migrate** for database migrations, which are automatically applied at runtime.

### When Do I Need to Worry About Migrations?

- **After the First Setup**: Migrations are automatically handled each time the application starts, so you don’t need to run `flask db upgrade` manually.
- **When You Change Models**: If you modify the database models in `app.py` (for example, adding new fields), you will need to generate and apply a new migration manually.

### Manually Generating Migrations (When Modifying Models)

1. **Generate a Migration**:
   If you've made changes to your database models (like adding a new table or column), run the following command to generate a migration file:

   ```bash
   docker compose run flaskapp flask db migrate -m "Description of the change"
   ```

2. **Apply the Migration**:
   Once the migration is generated, simply restart the application with:
   ```bash
   docker compose up
   ```
   The migration will be applied automatically via the `flask db upgrade` command in the Dockerfile.

---

## Stopping and Restarting the Application

To stop the running containers, use:

```bash
docker compose down
```

To restart the application, use:

```bash
docker compose up
```

If you make changes to the code or the `Dockerfile`, rebuild the containers with:

```bash
docker compose up --build
```

---

## Accessing the PostgreSQL Database

To connect to the PostgreSQL database running in Docker, use any PostgreSQL client (like **pgAdmin**, **DBeaver**, etc.) with the following connection details:

- **Host**: `localhost`
- **Port**: `5432`
- **User**: `postgres`
- **Password**: `password`
- **Database**: `mydatabase`

---

## File Structure

### 1. `app.py`

This file contains the Flask application, including the model (`User`), routes, and database integration. The `User` model has two fields: `id` and `username`.

### 2. `Dockerfile`

This file defines how the Flask application is built into a Docker image. It installs dependencies and runs the Flask app. Additionally, it runs database migrations automatically using the command:

```bash
CMD ["sh", "-c", "flask db upgrade && flask run --host=0.0.0.0 --port=4000"]
```

This ensures that database migrations are applied every time the app starts.

### 3. `docker-compose.yml`

This file defines the services for Docker Compose:

- **flaskapp**: The Flask application, which depends on the `db` service.
- **db**: The PostgreSQL database.

Volumes are configured to persist both the database data and the migration files.

### 4. `requirements.txt`

This file lists all the dependencies required for the Flask application, including:

- `flask`
- `Flask-SQLAlchemy`
- `Flask-Migrate`
- `Flask-CORS`
- `psycopg2-binary` (for PostgreSQL support)

---

## Additional Information

- The application runs on **port 4000** for the Flask API.
- PostgreSQL runs on **port 5432**.

---

### Summary

- **First-time setup** requires initializing migrations with `flask db init`.
- Migrations are automatically applied on startup, so you don’t need to manually run them unless you modify the models.
- The application is accessible at `http://localhost:4000` after running `docker compose up`.

This setup allows for easy management of both the application and the database, with Docker simplifying the entire process.

---
