## Run with Docker

> ✅ Only Docker is required to build and run the application. No other dependencies needed.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fetch-reward.git
cd fetch-reward
```

### 2. Build the Docker image

```bash
docker build -t receipt-processor .
```

### 3. Run the application

```bash
docker run -p 8000:8000 receipt-processor
```

### 4. Access the API

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

