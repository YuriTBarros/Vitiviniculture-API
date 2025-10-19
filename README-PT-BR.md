<h2 align = "right"> Selecione o idioma:</h2>

[<img align="right"  width="30px" src="https://github.com/yammadev/flag-icons/blob/master/svg/US.svg" />](https://github.com/YuriTBarros/Vitiviniculture-API/blob/master/README.md)
[<img align="right" width="30px" src="https://github.com/yammadev/flag-icons/blob/master/svg/BR.svg"/>](https://github.com/YuriTBarros/Vitiviniculture-API/blob/master/README-PT-BR.md)
<p align = "right"> Idioma:</p>

---

# 🍇 🍇 🍇 Vitiviniculture API — FastAPI + Scrapers + Docker 

![GitHub Actions](https://github.com/IgorComune/tech_challenge_ml_engineer/actions/workflows/verify.yml/badge.svg) ![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)

## Introdução ao Projeto

### Descrição Geral

Este projeto é uma API RESTful construída com **FastAPI**, projetada para servir dados relacionados à vitivinicultura (produção de vinho) no Brasil. Ele emprega *web scrapers* para coletar automaticamente dados públicos de fontes como o site da **Embrapa Vitivinicultura**, processa-os e os armazena em um cache local.

A API fornece *endpoints* autenticados para várias categorias de dados — incluindo produção, processamento, importação, exportação e comercialização — disponibilizando os dados prontamente em formato JSON ou CSV para análise, visualização ou consumo por futuros modelos de *machine learning*.

### Contexto Acadêmico

Este projeto foi desenvolvido como a entrega da **Fase 1** da **Pós-Graduação em Machine Learning Engineering (Postech) da Fiap**. O objetivo principal foi aplicar princípios de engenharia de dados para construir um *pipeline* de dados robusto, desde a coleta (*scraping*) e processamento até o *deploy* da API, criando uma fonte de dados fundamental para projetos subsequentes do curso.

##  👥 Membros da Equipe

Este projeto foi desenvolvido em colaboração pelos seguintes membros:

* **Felippe Maurício** - ([@felippemauricio](https://github.com/felippemauricio))
* **Igor Comune** - ([@IgorComune](https://github.com/IgorComune))
* **Mario Gotta** - ([@MariolGotta](https://github.com/MariolGotta))
* **Yuri T. de Barros** - ([@YuriTBarros](https://github.com/YuriTBarros))

---


## 🏁 Começando

Esta API fornece dados relacionados à vitivinicultura, incluindo produção, processamento, importação, exportação e comercialização. Os dados são coletados de fontes públicas usando *web scrapers*, principalmente do site da Embrapa Vitivinicultura: [http://vitibrasil.cnpuv.embrapa.br](http://vitibrasil.cnpuv.embrapa.br), e servidos através de uma interface RESTful.

## 📁 Estrutura do Projeto

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
## 🚀 Funcionalidades

- 🔐 Autenticação de usuário e acesso baseado em token  
- 🕸️ *Web scrapers* para coletar dados do mundo real  
- 📊 Categorização dos dados de vitivinicultura  
- 🌐 *Endpoints* da API REST para:  
  - Produção  
  - Processamento  
  - Importação  
  - Exportação  
  - Comercialização

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+** - **FastAPI** - **SQLite** - **Docker** - **Uvicorn** - **Makefile (para automação)**

## ⚙️ Instalação

### 🐳 Opção 1 — Com Docker 

```bash
# Clone o repositório
git clone [https://github.com/IgorComune/tech_challenge_ml_engineer](https://github.com/IgorComune/tech_challenge_ml_engineer)
cd tech_challenge_ml_engineer/vitivinicultura-api/

# Crie o arquivo .env
echo 'SECRET_KEY="SUA_CHAVE_PESSOAL_AQUI"' >> .env

# Construa e execute com Docker
docker build -t vitiviniculture-api .
docker run -p 8000:8000 vitiviniculture-api
```

### 💻 Opção 2 — Setup local
```bash
# Clone o repositório
git clone [https://github.com/IgorComune/tech_challenge_ml_engineer](https://github.com/IgorComune/tech_challenge_ml_engineer)
cd tech_challenge_ml_engineer/vitivinicultura-api/

# Crie o arquivo .env
echo 'SECRET_KEY="SUA_CHAVE_PESSOAL_AQUI"' >> .env

# Crie e ative o ambiente virtual
# Linux/macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute a API
uvicorn api.main:app --reload
```
### 🧰 Opção 3 — Alternativa (Makefile)
```bash
# Clone o repositório
git clone [https://github.com/IgorComune/tech_challenge_ml_engineer](https://github.com/IgorComune/tech_challenge_ml_engineer)
cd tech_challenge_ml_engineer/vitivinicultura-api/

# Crie o arquivo .env
echo 'SECRET_KEY="SUA_CHAVE_PESSOAL_AQUI"' >> .env

# Makefile
make venv       # Cria o ambiente virtual
make install    # Instala as dependências
make run        # Executa a API
```

## 📌 Endpoints

| Método | Endpoint                | Descrição                                 | Filtros           | Respostas          |
| ------ | ----------------------- | ------------------------------------------| ------------------| -------------------|
| POST   | `/auth/register`        | Registrar um novo usuário                 |                   | `{}` JSON          |
| POST   | `/auth/login`           | Obter token JWT                           |                   | `{}` JSON          |
| GET    | `/category`             | Lista de categorias disponíveis           |                   | `{}` JSON          |
| GET    | `/category/exportation` | Dados de exportação (servidos do cache local) | `year` (opcional) | `{}` JSON, 🟩📊 CSV |
| GET    | `/category/importation` | Dados de importação (servidos do cache local) | `year` (opcional) | `{}` JSON, 🟩📊 CSV |
| GET    | `/category/production`  | Dados de produção (servidos do cache local)   | `year` (opcional) | `{}` JSON, 🟩📊 CSV |
| GET    | `/category/processing`  | Dados de processamento (servidos do cache local) | `year` (opcional) | `{}` JSON, 🟩📊 CSV |
| GET    | `/category/trade`       | Dados de comercialização (servidos do cache local) | `year` (opcional) | `{}` JSON, 🟩📊 CSV |


- Acesse a documentação em [http://localhost:8000/docs](http://localhost:8000/docs) em desenvolvimento  
- Ou acesse o ambiente de produção hospedado no [Render](https://render.com) em [https://vitiviniculture-api.onrender.com/docs](https://vitiviniculture-api.onrender.com/docs)  

## 🧪 Desenvolvimento

### 🔧 Comandos do Makefile
```bash
make venv     # Cria virtualenv
make install  # Instala dependências
make run      # Inicia API (dev)
make lint     # Executa checagem de estilo (flake8)
make format   # Formata o código (black + isort)
```

### ✅ CI/CD

O GitHub Actions executa o fluxo de trabalho [`verify.yml`](.github/workflows/verify.yml) em cada *pull request* para garantir a qualidade e a formatação do código. O fluxo de trabalho consiste em três fases:

1. **Lint** — verifica o estilo e a formatação do código  
2. **Build Docker** — testa se a construção do Docker é concluída com sucesso  
3. **Deploy to Render** — faz o *deploy* automaticamente para o ambiente de produção - executa apenas na *branch* `main`

## 🧱 Arquitetura

Nosso projeto consiste em uma API e um serviço em segundo plano. Quando o projeto é iniciado, tanto a API quanto o serviço em segundo plano são lançados. A cada 10 minutos, o serviço em segundo plano rastreia o site da Embrapa e atualiza os dados localmente, armazenando-os em um cache nos formatos de arquivo JSON e CSV.

Todas as operações de leitura da API recuperam dados desse cache local para minimizar impactos no desempenho e evitar dependência do site da Embrapa, que às vezes pode estar offline.

Além disso, todos os *endpoints* de leitura são protegidos e exigem autenticação baseada em JWT para garantir acesso seguro.

![Arquitetura do Projeto](httpss://cdn.discordapp.com/attachments/1374899745033687121/1374899824859676752/Inserir_um_titulo.png?ex=683457fe&is=6833067e&hm=cc5102426aa55870be81004dc73367375b909f6b9bc9a9e8cf178e58f9df2eae)

## 🤝 Contribuindo

1. Faça um *fork* do projeto  
2. Crie uma *branch* para sua funcionalidade (`git checkout -b feature/nova-feature`)  
3. Faça *commit* das suas alterações (`git commit -m 'Adiciona nova feature'`)  
4. Faça *push* para a *branch* (`git push origin feature/nova-feature`)  
5. Abra um *Pull Request* Veja o *template* de *pull request* em [pull_request_template.md](.github/pull_request_template.md) para mais informações sobre como contribuir.

## 🧪 Exemplos com Postman

Aqui estão exemplos de requisições para cada *endpoint* usando o Postman.

### 1. Registrar - `/auth/register`

**Endpoint**: POST `httpss://vitiviniculture-api.onrender.com/auth/register`
```bash
curl --location 'httpss://[vitiviniculture-api.onrender.com/auth/register](https://vitiviniculture-api.onrender.com/auth/register)' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "seu_usuario",
    "password": "sua_senha"
}'
```
### 2. Login - `/auth/login`

**Endpoint**: POST `https://vitiviniculture-api.onrender.com/auth/login`
```bash
curl --location '[https://vitiviniculture-api.onrender.com/auth/login](https://vitiviniculture-api.onrender.com/auth/login)' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'username=seu_usuario' \
--data-urlencode 'password=sua_senha'
```

### 3. Listar categorias - `/category`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category`
```bash
curl --location '[https://vitiviniculture-api.onrender.com/category](https://vitiviniculture-api.onrender.com/category)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'
```

### 4. Exportação - `/category/exportation`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/exportation`
```bash
# `{}` JSON 
curl --location '[https://vitiviniculture-api.onrender.com/category/exportation](https://vitiviniculture-api.onrender.com/category/exportation)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - com filtro de ano
curl --location '[https://vitiviniculture-api.onrender.com/category/exportation?year=2002](https://vitiviniculture-api.onrender.com/category/exportation?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location '[https://vitiviniculture-api.onrender.com/category/exportation](https://vitiviniculture-api.onrender.com/category/exportation)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - com filtro de ano
curl --location '[https://vitiviniculture-api.onrender.com/category/exportation?year=2002](https://vitiviniculture-api.onrender.com/category/exportation?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'
```

### 5. Importação - `/category/importation`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/importation`
```bash
# `{}` JSON 
curl --location '[https://vitiviniculture-api.onrender.com/category/importation](https://vitiviniculture-api.onrender.com/category/importation)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - com filtro de ano
curl --location '[https://vitiviniculture-api.onrender.com/category/importation?year=2002](https://vitiviniculture-api.onrender.com/category/importation?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location '[https://vitiviniculture-api.onrender.com/category/importation](https://vitiviniculture-api.onrender.com/category/importation)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - com filtro de ano
curl --location '[https://vitiviniculture-api.onrender.com/category/importation?year=2002](https://vitiviniculture-api.onrender.com/category/importation?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'

```
### 6. Produção - `/category/production`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/production`
```bash
# `{}` JSON 
curl --location '[https://vitiviniculture-api.onrender.com/category/production](https://vitiviniculture-api.onrender.com/category/production)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - com filtro de ano
curl --location '[https://vitiviniculture-api.onrender.com/category/production?year=2002](https://vitiviniculture-api.onrender.com/category/production?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location '[https://vitiviniculture-api.onrender.com/category/production](https://vitiviniculture-api.onrender.com/category/production)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - com filtro de ano
curl --location '[https://vitiviniculture-api.onrender.com/category/production?year=2002](https://vitiviniculture-api.onrender.com/category/production?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'
```

### 7. Processamento - `/category/processing`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/processing`
```bash
# `{}` JSON 
curl --location '[https://vitiviniculture-api.onrender.com/category/processing](https://vitiviniculture-api.onrender.com/category/processing)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - com filtro de ano
curl --location 'httpss://[vitiviniculture-api.onrender.com/category/processing?year=2002](https://vitiviniculture-api.onrender.com/category/processing?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location '[https://vitiviniculture-api.onrender.com/category/processing](https://vitiviniculture-api.onrender.com/category/processing)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - com filtro de ano
curl --location 'httpss://[vitiviniculture-api.onrender.com/category/processing?year=2002](https://vitiviniculture-api.onrender.com/category/processing?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'
```

### 8. Comercialização - `/category/trade`

**Endpoint**: GET `https://vitiviniculture-api.onrender.com/category/trade`
```bash
# `{}` JSON 
curl --location '[https://vitiviniculture-api.onrender.com/category/trade](https://vitiviniculture-api.onrender.com/category/trade)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# `{}` JSON - com filtro de ano
curl --location '[https://vitiviniculture-api.onrender.com/category/trade?year=2002](https://vitiviniculture-api.onrender.com/category/trade?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: application/json'

# 🟩📊 CSV
curl --location '[https://vitiviniculture-api.onrender.com/category/trade](https://vitiviniculture-api.onrender.com/category/trade)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'

# 🟩📊 CSV - com filtro de ano
curl --location '[https://vitiviniculture-api.onrender.com/category/trade?year=2002](https://vitiviniculture-api.onrender.com/category/trade?year=2002)' \
--header 'Authorization: Bearer seu-jwt-token' \
--header 'Accept: text/csv'
```

## 📄 Licença

Este projeto está licenciado sob os termos incluídos no arquivo [LICENSE](LICENSE).


