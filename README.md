<p align="center">
  <img src="media/7kvp.gif" alt="Fitness App Animation" width="600"/>
</p>


<h1 align="center">🏋️‍♂️ Fitness Manager App</h1>

<p align="center">
  <strong>Powerful full-stack fitness backend</strong> built with FastAPI, SQLAlchemy, MySQL & Docker.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.95.1-green?style=flat-square&logo=fastapi" />
  <img src="https://img.shields.io/badge/MySQL-8.0-blue?style=flat-square&logo=mysql" />
  <img src="https://img.shields.io/badge/Docker-Containerized-blue?style=flat-square&logo=docker" />
  <img src="https://img.shields.io/badge/Redis-Caching-red?style=flat-square&logo=redis" />
</p>

---

## 🚀 Features

### 🔐 Authentication & Authorization
- Role-specific JWT-based signup/login for **Client**, **Trainer**, and **Owner**  
- Passwords securely hashed using **bcrypt**  
- Token blacklisting using **Redis** for secure logout  
- **Swagger UI** integration for easy API testing  

### 👥 Role-Based Access
- **Clients**: View workouts & diets, calculate BMI/BMR  
- **Trainers**: Assign workouts based on membership tier & specialization  
- **Owners**: Upload gym images via Cloudinary, manage clients/trainers  

### 🏋️ Workout & Diet Management
- Many-to-many relationships between clients and diet types  
- Supported diet types: *Vegetarian, Vegan, Eggitarian, Mediterranean*  
- Workouts include: reps, sets, duration, calories burned  
- Trainers assigned based on membership tier & specialization  

### 🧾 Membership System
- Tiered memberships: *Basic, Gold, Platinum*  
- Higher tiers unlock more advanced workouts  
- Seed membership data into MySQL via Docker  

### ☁️ Cloudinary Integration
- Upload and store gym images securely  
- Fetch and display images using Cloudinary public URLs  

---

## 🧱 Tech Stack

| Tech            | Description                                 |
|-----------------|---------------------------------------------|
| FastAPI         | Modern Python web framework                 |
| SQLAlchemy      | ORM for interacting with MySQL              |
| MySQL           | Relational database backend                 |
| Docker          | Containerization & environment setup        |
| Redis           | Token blacklisting and caching              |
| Cloudinary      | Gym image uploads and storage               |
| JWT             | Secure access tokens with expiration        |

---

## 📂 Project Structure

```
healthTrackerApp/
├── main.py
├── database.py
├── dependencies.py
├── models/
│   ├── client/
│   ├── owner/
│   ├── trainer/
│   └── utils/
├── routes/
│   ├── auth/
│   ├── core/
│   ├── general/
│   └── users/
├── schemas/
│   ├── client.py
│   ├── trainer.py
│   ├── owner.py
│   ├── membership.py
│   └── diet.py
├── auth/
│   ├── auth.py
│   ├── client_auth_utils.py
│   ├── trainer_auth_utils.py
│   └── owner_auth_utils.py
├── utils/
│   └── redis_connection.py
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fitness-manager-app.git
cd fitness-manager-app
```

### 2. Create a `.env` file in the root directory:
```env
DATABASE_URL=mysql+mysqlconnector://root:yourpassword@db/fitness_db
SECRET_KEY=your_jwt_secret_key
REDIS_URL=redis://redis:6379
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 3. Start the Application Using Docker
```bash
docker-compose up --build
```

### 4. Access API Docs
Open: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔌 API Endpoints (Highlights)

| Endpoint                    | Description                            |
|----------------------------|----------------------------------------|
| `/auth/client/signup`      | Register a new client                  |
| `/auth/client/login`       | Login client                           |
| `/auth/client/logout`      | Logout and blacklist token             |
| `/auth/trainer/signup`     | Register a new trainer                 |
| `/auth/owner/signup`       | Register gym owner                     |
| `/client/assign-diet`      | Assign diets to a client               |
| `/trainer/assign-workout`  | Assign workouts to a client            |
| `/gym/upload-photo`        | Upload gym image via Cloudinary        |
| `/membership/create`       | Create or fetch membership tiers       |

---

## 📦 Seed Membership Data

To pre-load membership tiers into MySQL, include sample data in your SQL seed script and mount it in Docker. *(Sample SQL coming soon)*

---

## 🧠 Health Calculations Supported

- ✅ BMI (Body Mass Index)  
- ✅ BMR (Basal Metabolic Rate)  
- ✅ Macronutrient Distribution Ratio (MDR)  

---

## 🧪 Testing & Dev Tools

- **Swagger Docs**: `/docs`  
- **Postman Collection**: *Coming Soon*  
- **Other Tools**: Docker, Redis, GitHub Actions, Cloudinary, Android Studio *(for future mobile integration)*

---

## 🙌 Contributions

Pull requests, issues, and feature suggestions are welcome!  
If you find this project helpful, don’t forget to ⭐ it and share it.

---

## 👤 Author

**Gourav Sharma**  
📫 [LinkedIn](#) | 💻 *Portfolio Coming Soon*

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.

