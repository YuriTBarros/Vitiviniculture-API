# 🍇 🍇 🍇 Vitiviniculture API — FastAPI + Scrapers + Docker 

![GitHub Actions](https://github.com/IgorComune/tech_challenge_ml_engineer/actions/workflows/verify.yml/badge.svg) ![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)

## 🏁 Getting Started

This API provides data related to vitiviniculture, including production, processing, import, export, and trade. Data is collected from public sources using web scrapers, primarily from the Embrapa Vitiviniculture website: [http://vitibrasil.cnpuv.embrapa.br](http://vitibrasil.cnpuv.embrapa.br), and served through a RESTful interface.

## 📁 Project Structure

```
vitiviniculture-api/
├── api/                            # Main API code
│   ├── background_jobs/            # Background jobs
│   ├── core/                       # Configuration and security
│   ├── exceptions/                 # Custom exceptions
│   ├── models/                     # Data models
│   ├── routes/                     # API routes
│   ├── schemas/                    # Validation schemas
│   ├── services/                   # Services and scrapers
|   └── main.py                     # API entry point
├── data/                           # Collected data in CSV and JSON
├── database/                       # Database configuration
├── docs/                           # Documentation
├── requirements.txt                # Project dependencies
└── .env                            # Environment variables (you must create this)
```

## 🚀 Features

- 🔐 User authentication and token-based access  
- 🕸️ Web scrapers to collect real-world data  
- 📊 Categorization of vitiviniculture data  
- 🌐 REST API endpoints for:  
  - Production  
  - Processing  
  - Import  
  - Export  
  - Trade

## 🛠️ Tech Stack

- **Python 3.11+**  
- **FastAPI**  
- **SQLite**  
- **Docker**  
- **Uvicorn**  
- **Makefile (for automation)**

## ⚙️ Installation

### 🐳 Option 1 — With Docker 

```bash
# Clone the repository
git clone https://github.com/IgorComune/tech_challenge_ml_engineer
cd tech_challenge_ml_engineer/vitivinicultura-api/

# Create .env file
echo 'SECRET_KEY="YOUR_PERSONAL_KEY_HERE"' >> .env

# Build and run with Docker
docker build -t vitiviniculture-api .
docker run -p 8000:8000 vitiviniculture-api
```

### 💻 Option 2 — Local Setup

```bash
# Clone the repository
git clone https://github.com/IgorComune/tech_challenge_ml_engineer
cd tech_challenge_ml_engineer/vitivinicultura-api/

# Create .env file
echo 'SECRET_KEY="YOUR_PERSONAL_KEY_HERE"' >> .env

# Create and activate virtual environment
# Linux/macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn api.main:app --reload
```
### 🧰 Option 3 — Alternative (Makefile)

If you prefer using make, you can use:

```bash
# Clone the repository
git clone https://github.com/IgorComune/tech_challenge_ml_engineer
cd tech_challenge_ml_engineer/vitivinicultura-api/

# Create .env file
echo 'SECRET_KEY="YOUR_PERSONAL_KEY_HERE"' >> .env

# Makefile
make venv       # Create virtual environment
make install    # Install dependencies
make run        # Run the API
```

## 📌 Endpoints

| Method | Endpoint                | Description                               | Filters           | Responses          |
| ------ | ----------------------- | ------------------------------------------| ------------------| -------------------|
| POST   | `/auth/register`        | Register a new user                       |                   | `{}` JSON          |
| POST   | `/auth/login`           | Get JWT token                             |                   | `{}` JSON          |
| GET    | `/category/exportation` | Export data (served from local cache)     | `year` (optional) | `{}` JSON, 🟩📊 CSV |
| GET    | `/category/importation` | Import data (served from local cache)     | `year` (optional) | `{}` JSON, 🟩📊 CSV |
| GET    | `/category/production`  | Production data (served from local cache) | `year` (optional) | `{}` JSON, 🟩📊 CSV |
| GET    | `/category/processing`  | Processing data (served from local cache) | `year` (optional) | `{}` JSON, 🟩📊 CSV |
| GET    | `/category/trade`       | Trade data (served from local cache)      | `year` (optional) | `{}` JSON, 🟩📊 CSV |



- Access the docs at [http://localhost:8000/docs](http://localhost:8000/docs) in development  
- Or access the production environment hosted on [Render](https://render.com) at [https://vitiviniculture-api.onrender.com/docs](https://vitiviniculture-api.onrender.com/docs)  

## 🧪 Development

### 🔧 Makefile Commands
```bash
make venv     # Create virtualenv
make install  # Install dependencies
make run      # Start API (dev)
make lint     # Run code style check (flake8)
make format   # Format code (black + isort)
```

### ✅ CI/CD

GitHub Actions runs the [`verify.yml`](.github/workflows/verify.yml) workflow on each pull request to ensure code quality and formatting. The workflow consists of three phases:

1. **Lint** — checks code style and formatting  
2. **Build Docker** — tests if the Docker build completes successfully  
3. **Deploy to Render** — automatically deploys to the production environment - only runs on the `main` branch

## 🧱 Architecture

![Project Architecture](https://cdn.discordapp.com/attachments/1374899745033687121/1374899824859676752/Inserir_um_titulo.png?ex=683457fe&is=6833067e&hm=cc5102426aa55870be81004dc73367375b909f6b9bc9a9e8cf178e58f9df2eae)

## 🤝 Contributing

1. Fork the project  
2. Create a branch for your feature (`git checkout -b feature/new-feature`)  
3. Commit your changes (`git commit -m 'Add new feature'`)  
4. Push to the branch (`git push origin feature/new-feature`)  
5. Open a Pull Request  

See the pull request template in [pull_request_template.md](.github/pull_request_template.md) for more information on how to contribute.

## 🧪 Postman Examples

Here are example requests for each endpoint using Postman.

### 1. Register - `/auth/register`

**Endpoint**: POST `https://vitiviniculture-api.onrender.com/auth/register`
```bash
curl --location 'https://vitiviniculture-api.onrender.com/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "your_username",
    "password": "your_password"
}'
```

### 2. Login - `/auth/login`

**Endpoint**: POST `https://vitiviniculture-api.onrender.com/auth/login`
```bash
curl --location 'https://vitiviniculture-api.onrender.com/auth/login' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=your_username' \
--data-urlencode 'password=your_password'
```

### 3. Exportation - `/category/exportation`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/exportation`
```bash
# `{}` JSON 
curl --location 'https://vitiviniculture-api.onrender.com/category/exportation' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/exportation?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location 'https://vitiviniculture-api.onrender.com/category/exportation' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/exportation?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'
```

### 4. Importation - `/category/importation`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/importation`
```bash
# `{}` JSON 
curl --location 'https://vitiviniculture-api.onrender.com/category/importation' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/importation?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location 'https://vitiviniculture-api.onrender.com/category/importation' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/importation?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'
```

### 5. Production - `/category/production`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/production`
```bash
# `{}` JSON 
curl --location 'https://vitiviniculture-api.onrender.com/category/production' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/production?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location 'https://vitiviniculture-api.onrender.com/category/production' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/production?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'
```

### 6. Processing - `/category/processing`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/processing`
```bash
# `{}` JSON 
curl --location 'https://vitiviniculture-api.onrender.com/category/processing' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/processing?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location 'https://vitiviniculture-api.onrender.com/category/processing' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/processing?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'
```

### 7. Trade - `/category/trade`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/trade`
```bash
# `{}` JSON 
curl --location 'https://vitiviniculture-api.onrender.com/category/trade' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/trade?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location 'https://vitiviniculture-api.onrender.com/category/trade' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - with year filter
curl --location 'https://vitiviniculture-api.onrender.com/category/trade?year=2002' \
--header 'Authorization: Bearer your-jwt-token' \
--header 'Accept: text/csv'
```

## 📄 License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.

