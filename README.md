🏥 Patient Management System API
A production-style REST API built using FastAPI to manage patient records efficiently.
Supports full CRUD operations with automatic BMI calculation and health classification.

📌 1️⃣ Introduction
The Patient Management System API provides endpoints to manage patient data including:
Patient creation
Data retrieval
Updates
Deletion
Automatic BMI computation
Health status classification

Designed following clean backend architecture principles.
🚀 2️⃣ Features
✅ RESTful API architecture
✅ Full CRUD operations
✅ Automatic BMI calculation
✅ Health classification system
✅ Data validation using Pydantic
✅ Sorting by height, weight, or BMI
✅ Interactive Swagger & ReDoc documentation

⚙️ 3️⃣ Getting Started
📦 Requirements
Python 3.8+
FastAPI
Uvicorn

🔧 Installation
git clone https://github.com/YOUR-USERNAME/patient-management-api.git
cd patient-management-api

python -m venv venv
venv\Scripts\activate   # Windows

pip install fastapi uvicorn
▶️ 4️⃣ Run Server
uvicorn main:app --reload

Server will start at:

http://127.0.0.1:8000
📖 API Documentation
Swagger UI → http://127.0.0.1:8000/docs
ReDoc → http://127.0.0.1:8000/redoc

🔐 Authentication
Currently, the API does not implement authentication.
All endpoints are publicly accessible.
Future scope: JWT-based authentication integration.

📌 API Endpoints
Method	Endpoint	Description
GET	/	Home route
GET	/about	About API
GET	/view	View all patients
GET	/patient/{id}	Get patient by ID
POST	/create	Create new patient
PUT	/update/{id}	Update patient
DELETE	/delete/{id}	Delete patient
GET	/sort	Sort patients

Example:
GET /sort?sort_by=bmi&order=desc
💻 Example cURL Requests
🟢 Create Patient
curl -X POST http://127.0.0.1:8000/create \
-H "Content-Type: application/json" \
-d '{
  "id": "P001",
  "name": "Ashish Shetty",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70
}'

🧮 BMI Calculation
BMI = weight / (height²)
BMI Range	Classification
< 18.5	Underweight
18.5 – 24.9	Normal
25 – 29.9	Overweight
≥ 30	Obese

🛠️ Tech Stack
🐍 Python
⚡ FastAPI
📦 Pydantic
🚀 Uvicorn
🗂️ JSON (File-based persistence)

📄 License
This project is licensed under the MIT License.
