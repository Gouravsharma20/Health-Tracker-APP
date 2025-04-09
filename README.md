
# 🏋️‍♂️ Fitness Manager App

A powerful full-stack backend system built with **FastAPI**, **SQLAlchemy**, **MySQL**, and **Docker** for managing health and fitness efficiently. Designed for **clients**, **trainers**, and **gym owners**, the app provides role-based access, personalized workout & diet plans, secure JWT authentication, Redis-based token blacklisting, and Cloudinary image support.

---

## 🚀 Features

### 🔐 Authentication & Authorization
- Role-specific JWT-based signup/login for **Client**, **Trainer**, and **Owner**
- Passwords securely hashed using bcrypt
- Token blacklisting using Redis for safe logout
- Swagger UI integration for API testing

### 👥 Role-Based Access
- **Clients**: View workouts & diets, calculate BMI/BMR
- **Trainers**: Assign workouts based on membership tier & specialization
- **Owners**: Upload gym images via Cloudinary, manage clients/trainers

### 🏋️ Workout & Diet Management
- Many-to-many relationships between clients and diet types
- Support for diet types like: Vegetarian, Vegan, Eggitarian, Mediterranean
- Workouts contain: reps, sets, duration, calories burned
- Trainers assigned based on membership tier & specialization

### 🧾 Membership System
- Tiered memberships (e.g., Basic, Gold, Platinum)
- Higher tiers unlock access to more advanced workouts
- Seed membership data via Docker-MySQL

### ☁️ Cloudinary Integration
- Upload and store gym images securely
- Fetch and display images with public URLs

---

## 🧱 Tech Stack

| Tech           | Description                          |
|----------------|--------------------------------------|
| **FastAPI**    | Modern Python web framework          |
| **SQLAlchemy** | ORM for interacting with MySQL       |
| **MySQL**      | Relational database backend          |
| **Docker**     | Containerization                     |
| **Redis**      | Blacklisting access tokens           |
| **Cloudinary** | Gym image uploads and storage        |
| **JWT**        | Secure access tokens with expiration |

---

## 📂 Project Structure

healthTrackerApp/ ├── main.py ├── database.py ├── dependencies.py ├── models/ │ ├── client/ │ ├── owner/ │ ├── trainer/ │ └── utils/ ├── routes/ │ ├── auth/ │ ├── core/ │ ├── general/ │ └── users/ ├── schemas/ │ ├── client.py │ ├── trainer.py │ ├── owner.py │ ├── membership.py │ └── diet.py ├── auth/ │ ├── auth.py │ ├── client_auth_utils.py │ ├── trainer_auth_utils.py │ └── owner_auth_utils.py ├── utils/ │ └── redis_connection.py ├── Dockerfile ├── docker-compose.yml ├── .env


---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/fitness-manager-app.git
cd fitness-manager-app


2. Create a .env file in the root directory:

DATABASE_URL=mysql+mysqlconnector://root:yourpassword@db/fitness_db
SECRET_KEY=your_jwt_secret_key
REDIS_URL=redis://redis:6379
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret


DATABASE_URL=mysql+mysqlconnector://root:yourpassword@db/fitness_db
SECRET_KEY=your_jwt_secret_key
REDIS_URL=redis://redis:6379
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret


3. Start the application using Docker

docker-compose up --build


4. Access API Docs
Visit: http://localhost:8000/docs

 API Endpoints (Highlights)
Endpoint	Description
/auth/client/signup	Register a new client
/auth/client/login	Login client
/auth/client/logout	Logout and blacklist token
/auth/trainer/signup	Register a new trainer
/auth/owner/signup	Register gym owner
/client/assign-diet	Assign diets to a client
/trainer/assign-workout	Assign workouts to a client
/gym/upload-photo	Upload gym image via Cloudinary
/membership/create	Create or fetch membership tiers


📦 Seed Membership Data
To pre-load membership tiers into MySQL:

sql
Copy
Edit


🧠 Health Calculations Supported
BMI (Body Mass Index)

BMR (Basal Metabolic Rate)

Macronutrient Distribution Ratio

🧪 Testing & Dev Tools
Swagger Docs: /docs

Postman Collection: [Coming Soon]

Tools: Docker, Redis, GitHub Actions, Cloudinary, Android Studio (for mobile integration)

🙌 Contributions
Contributions, issues and feature requests are welcome!
If you liked this project, ⭐ star it and share it.

👤 Author
Gourav Sharma
📫 LinkedIn
💻 Portfolio: Coming Soon

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.


