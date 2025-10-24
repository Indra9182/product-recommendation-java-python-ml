# ===== Stage 1: Build the Java app =====
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn -q -e -B -DskipTests dependency:go-offline
COPY src ./src
RUN mvn -q -e -B -DskipTests package

# ===== Stage 2: Run Java + Python together =====
FROM eclipse-temurin:17-jre
WORKDIR /app

# Copy built Java JAR
COPY --from=build /app/target/*.jar app.jar

# --- Install Python and dependencies ---
RUN apt-get update && apt-get install -y python3 python3-pip
COPY ../python-ml-service /app/python-ml-service
RUN pip install --no-cache-dir -r /app/python-ml-service/requirements.txt

# Environment + ports
ENV ML_SERVICE_URL=http://localhost:5001
EXPOSE 8080 5001

# Start Python microservice in background, then Java
CMD python3 /app/python-ml-service/app.py & \
    java -jar /app/app.jar
