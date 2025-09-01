# DavaX Math API

A JWT-secured RESTful microservice that allows users to perform core mathematical operations (**factorial**, **fibonacci**, and **power**) and logs each request with timestamped records. Built using Flask, this project follows clean microservice principles and offers API documentation via Swagger.

##  DevOps Homework Summary

This project was developed as part of a DevOps assignment focused on Docker-based containerization and Kubernetes deployment via Rancher Desktop.

###  What I did:

- Built a lightweight Python Flask web service with math operations
- Wrote a `Dockerfile` to containerize the app
- Used `docker-compose` for local development and testing
- Built the Docker image locally and ensured it runs successfully
- Wrote Kubernetes manifests (`deployment.yaml`, `service.yaml`)
- Deployed the container to a Rancher Desktop Kubernetes cluster
- Used port-forwarding to access the app from the host

---

### Commands I ran

#### Docker (local build & run)

```bash
docker build -t davax-api:latest .
docker-compose up --build
```

#### Kubernetes (Rancher Desktop)

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
kubectl get svc
kubectl port-forward service/davax-service 8080:80
```

Then opened the app at:  

http://localhost:8080

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
├── migrations/     → contains Alembic-generated database migration scripts
├── models/         → ORM models: User, Operation, OperationLog
├── routes/         → REST endpoints grouped by feature
├── schemas/        → Pydantic validation and serialization
├── services/       → Business logic (math functions, utilities)
├── k8s/            → Kubernetes manifests for application deployment and service exposure   
├── config.py       → App configuration (JWT secret, DB URI)
app.py              → App entry point
```

---

##  Libraries & Frameworks

- **Flask** – Micro web framework  
- **Flask-Smorest** – Blueprint-based API with Swagger documentation 
- **SQLAlchemy** – Database ORM (with SQLite backend)
- **Flask-SQLAlchemy** – Integration layer between Flask and SQLAlchemy   
- **Pydantic** – Request validation and serialization 
- **Flask-JWT-Extended** – JWT-based authentication  
- **Flask-Migrate** – Database schema migrations using Alembic  
- **Passlib** – Secure password hashing (e.g., bcrypt)  
- **Python-Dotenv** – Loads environment variables from `.env` files into Flask config
- **functools.lru_cache** – In-memory caching for performance optimization
## Author

Name : Ghiuta Cristian-Daniel

Location : Iasi (ISD)


