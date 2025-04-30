# 📝 Student Survey Microservices (Python Version)

A containerized, RESTful survey application built using **Django**, **Docker**, and **Jenkins CI/CD**. This microservice manages student survey data with full CRUD functionality and supports cloud-native deployment pipelines.

---

## 📦 Features

- Submit, retrieve, update, and delete student surveys
- REST API using Django REST Framework
- MySQL database integration
- Dockerized deployment
- Jenkins CI/CD automation pipeline
- AWS-compatible for EC2 and RDS

---

## 🚀 Live Demo

You can access the deployed API (if hosted) here:  
[https://54.84.79.35/k8s/.../api/surveys](https://54.84.79.35/k8s/clusters/c-m-7v596hpd/api/v1/namespaces/default/services/http:swe-micros-loadbalancer:8080/proxy/api/surveys)

---

## 🛠️ Tech Stack

- **Backend:** Django 5, Django REST Framework
- **Database:** MySQL (via `mysqlclient`)
- **Server:** Gunicorn
- **Containerization:** Docker
- **CI/CD:** Jenkins (with custom pipeline)
- **Hosting:** AWS EC2 & RDS
- **CORS Handling:** django-cors-headers

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Vrishin-Reddy/swe_microservices.git
cd swe_microservices/student_survey_project
```

### 2️⃣ Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file:
```
DEBUG=False
PORT=8080
ALLOWED_HOSTS=*
DB_NAME=yourdbname
DB_USER=yourdbuser
DB_PASSWORD=yourdbpassword
DB_HOST=yourdbhost
```

### 4️⃣ Run Migrations
```bash
python manage.py migrate
```

### 5️⃣ Start Server
```bash
gunicorn --bind 0.0.0.0:8080 student_survey_project.wsgi:application
```

Access: [http://localhost:8080/api/surveys](http://localhost:8080/api/surveys)

---

## 🐋 Docker Instructions

### Build and Run Locally:
```bash
docker build -t vrishin/student-survey-api-micro-python:new .
docker run -d -p 8080:8080 vrishin/student-survey-api-micro-python:new
```

---

## 🧪 API Endpoints

| Method | Endpoint             | Description         |
|--------|----------------------|---------------------|
| POST   | `/api/surveys`       | Create a new survey |
| GET    | `/api/surveys`       | Get all surveys     |
| GET    | `/api/surveys/{id}`  | Get survey by ID    |
| PUT    | `/api/surveys/{id}`  | Update survey       |
| DELETE | `/api/surveys/{id}`  | Delete survey       |

---

## 🔄 CI/CD Pipeline with Jenkins

This project includes a `Jenkinsfile` for automated builds, tests, and Docker deployment:

**Stages include:**
- Checkout & Setup
- Run Unit Tests
- Build Docker Image
- Push to Docker Hub
- Deploy on EC2

Customize environment via Jenkins parameters:
- `DEPLOY_ENV` (dev, staging, prod)
- `RUN_TESTS`, `DEPLOY`, `CUSTOM_TAG`

---

## 🧾 Database Setup (MySQL)

You can use [Amazon RDS](https://aws.amazon.com/rds/) or any hosted MySQL database. Ensure the DB credentials are included in your `.env` file.

---

## 📦 Project Structure

```
student_survey_project/
├── manage.py
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── .env
├── app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
```

---

## ⚠️ Notes

- Ensure CORS settings are appropriate for production (`CORS_ALLOW_ALL_ORIGINS=True` in dev only)
- Replace placeholder Docker credentials in the Jenkinsfile before production
- Jenkins uses `sudo` Docker commands – requires proper setup

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Contributors

- Vrishin Reddy Minkuri
- Rohith Reddy Marlapally
- Nikhil Kommineni
- Sharath Chandra Reddy Kottam
