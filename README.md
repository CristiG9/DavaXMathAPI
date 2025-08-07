# DavaX Math API

A JWT-secured RESTful microservice that allows users to perform core mathematical operations (**factorial**, **fibonacci**, and **power**) and logs each request with timestamped records. Built using Flask, this project follows clean microservice principles and offers API documentation via Swagger.

---

##  API Endpoints

###  Users

| Method | Endpoint            | Description                         |
|--------|---------------------|-------------------------------------|
| POST   | `/register`         | Register a new user                 |
| GET    | `/user/{user_id}`   | Retrieve user information by ID     |
| DELETE | `/user/{user_id}`   | Delete a user                       |
| POST   | `/login`            | Login and receive JWT token         |
| POST   | `/refresh`          | Refresh an access token             |
| POST   | `/logout`           | Logout and revoke token             |

---

###  Operations

| Method | Endpoint               | Description                                 |
|--------|------------------------|---------------------------------------------|
| GET    | `/operation`           | List all available operations               |
| POST   | `/operation`           | Create/register a new operation             |
| GET    | `/operation/{op_name}` | Get details for a specific operation        |
| DELETE | `/operation/{op_name}` | Delete an operation by name                 |

---

###  Operation Logs

| Method | Endpoint     | Description                              |
|--------|--------------|------------------------------------------|
| GET    | `/logs/me`   | Retrieve logs for the authenticated user |
| GET    | `/logs`      | Get all operation logs (admin/debug)     |
| POST   | `/factorial` | Compute factorial of an integer          |
| POST   | `/pow`       | Compute base raised to exponent          |
| POST   | `/fibonacci` | Compute the n-th Fibonacci number        |

---

##  Project Structure

```
app/
├── models/         → ORM models: User, Operation, OperationLog
├── routes/         → REST endpoints grouped by feature
├── schemas         → Marshmallow validation and serialization
├── services/       → Business logic (math functions, utilities)
├── config.py       → App configuration (JWT secret, DB URI)
run.py              → App entry point
```

---

##  Libraries & Frameworks

- **Flask** – Micro web framework  
- **Flask-Smorest** – API management + Swagger docs  
- **SQLAlchemy** – Database ORM (with SQLite backend)  
- **Flask-SQLAlchemy** – Integration layer between Flask and SQLAlchemy  
- **Marshmallow** – Request/response validation  
- **Flask-JWT-Extended** – JWT-based authentication  
- **Flask-Migrate** – Database schema migrations using Alembic  
- **Passlib** – Secure password hashing (e.g., bcrypt)  
- **Python-Dotenv** – Loads environment variables from `.env` files into Flask config  

## Author

Name : Ghiuta Cristian-Daniel 

Location : Iasi (ISD)


