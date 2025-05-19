# Vitiviniculture API

API for collecting, processing, and providing data related to vitiviniculture.

## About the Project

This project provides an API that gathers data on production, processing, import, and export in the vitiviniculture sector. The API uses scrapers to collect data from different sources and makes this data available through REST endpoints.

## Project Structure

```
vitiviniculture-api/
├── api/                            # Main API code
│   ├── background_jobs/            # Background jobs
│   ├── core/                       # Configuration and security
│   ├── exceptions/                 # Custom exceptions
│   ├── models/                     # Data models
│   ├── routes/                     # API routes
│   ├── schemas/                    # Validation schemas
│   └── services/                   # Services and scrapers
├── data/                           # Collected data in CSV and JSON
├── database/                       # Database configuration
├── docs/                           # Documentation
└── requirements.txt                # Project dependencies
```

## Features

- User authentication and authorization
- Automated collection of vitiviniculture data
- Categorization of collected data
- Endpoints for querying data on:
  - Production
  - Processing
  - Import
  - Export
  - Trade

## Technologies Used

- Python
- FastAPI (inferred from the structure)
- SQLite (database)
- Docker

## Installation and Setup

### Prerequisites

- Python 3.8+
- Docker (optional)

### Docker Installation

```bash
# Clone the repository
git clone https://github.com/IgorComune/vitiviniculture-api.git
cd vitiviniculture-api

# Build and run with Docker
docker build -t vitiviniculture-api .
docker run -p 8000:8000 vitiviniculture-api
```

### Local Installation

```bash
# Clone the repository
git clone https://github.com/IgorComune/vitiviniculture-api.git
cd vitiviniculture-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the API
python -m api.main
```

## Usage

After starting the API, you can access it at:

- `http://localhost:8000` (local development)
- `https://vitiviniculture-api.onrender.com/docs` (production)

### Main Endpoints

- `/auth/token` - Get authentication token  
- `/categories` - List available categories  
- `/exportation` - Export data  
- `/importation` - Import data  
- `/production` - Production data  
- `/processing` - Processing data  
- `/trade` - Trade data

For more details about the available endpoints, see the [API documentation](docs/api.md).

## Development

### Makefile

The project includes a Makefile to facilitate common development tasks:

```bash
# Run tests
make test

# Check code style (flake8)
make lint

# Start development environment
make dev
```

### Git Workflow

The project uses GitHub Actions for automatic code verification. When submitting a pull request, the `verify.yml` workflow will run to ensure code quality.

## Documentation

- [API Documentation](docs/api.md)
- [System Architecture](docs/architecture.md)

## License

This project is licensed under the terms included in the [LICENSE](LICENSE) file.

## Contributing

1. Fork the project  
2. Create a branch for your feature (`git checkout -b feature/new-feature`)  
3. Commit your changes (`git commit -m 'Add new feature'`)  
4. Push to the branch (`git push origin feature/new-feature`)  
5. Open a Pull Request  

See the pull request template in [.github/pull_request_template.md](.github/pull_request_template.md) for more information on how to contribute.

## Examples (Postman)

Here are example requests for each endpoint using Postman.

### 1. Authentication - `/auth/token`

**Method**: POST  
**URL**: `https://vitiviniculture-api.onrender.com/auth/token`  
**Body (x-www-form-urlencoded)**:
```
username: your_username
password: your_password
```

---

### 2. Categories - `/categories`

**Method**: GET  
**URL**: `https://vitiviniculture-api.onrender.com/categories`  
**Headers**:
```
Authorization: Bearer <your_token>
```

---

### 3. Exportation - `/exportation`

**Method**: GET  
**URL**: `https://vitiviniculture-api.onrender.com/exportation`  
**Headers**:
```
Authorization: Bearer <your_token>
```

---

### 4. Importation - `/importation`

**Method**: GET  
**URL**: `https://vitiviniculture-api.onrender.com/importation`  
**Headers**:
```
Authorization: Bearer <your_token>
```

---

### 5. Production - `/production`

**Method**: GET  
**URL**: `https://vitiviniculture-api.onrender.com/production`  
**Headers**:
```
Authorization: Bearer <your_token>
```

---

### 6. Processing - `/processing`

**Method**: GET  
**URL**: `https://vitiviniculture-api.onrender.com/processing`  
**Headers**:
```
Authorization: Bearer <your_token>
```

---

### 7. Trade - `/trade`

**Method**: GET  
**URL**: `https://vitiviniculture-api.onrender.com/trade`  
**Headers**:
```
Authorization: Bearer <your_token>
```
