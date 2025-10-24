# 🔗 Personalized Product Recommendation Engine (Java + Python Hybrid)

Master’s-level hybrid system combining a **Java Spring Boot** API with a **Python ML microservice** for real-time product recommendations (item-based collaborative filtering).

## 🧱 Architecture
```
+----------------------+         HTTP (Docker network)         +-------------------------+
|  Java Spring Boot    |  --->  http://ml-service:5001  --->  |  Python ML Microservice |
|  (REST API Gateway)  |         /recommend?user_id=...        |  (Flask + CF Model)     |
+----------+-----------+                                       +-----------+-------------+
           |                                                               |
           +----------------------- docker-compose -------------------------+
```

## 🚀 Quick Start (Docker)
```bash
docker compose up --build
```
- Java API: http://localhost:8080/api/recommendations/1
- Python ML: http://localhost:5001/recommend?user_id=1
- Train (optional): POST http://localhost:5001/train

## 📁 Project Structure
```
reco-hybrid-java-python/
├── docker-compose.yml
├── README.md
├── python-ml-service/
│   ├── app.py
│   ├── train.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── models/ (artifacts saved here after training)
└── java-api/
    ├── Dockerfile
    ├── pom.xml
    └── src/main/java/com/example/reco/...
```

## 📦 Tech Stack
- **Python ML:** Flask, Pandas, NumPy, scikit-learn (item-based cosine similarity)
- **Java API:** Spring Boot (Web), RestTemplate
- **Orchestration:** Docker Compose

## 🧪 Sample API
```bash
# Java API (proxy to Python ML)
curl http://localhost:8080/api/recommendations/1

# Python ML directly
curl "http://localhost:5001/recommend?user_id=1&k=5"
```

## 🧠 Notes
- The ML service generates a small synthetic user–item interaction dataset on first `/train`. If absent, it auto-trains on startup.
- Extend easily to use real data, MongoDB, or Redis caching.
