# Pipeline CI/CD Lab

[![CI/CD Pipeline](https://github.com/eringui/pipeline-cicd-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/eringui/pipeline-cicd-lab/actions/workflows/ci.yml)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![LocalStack](https://img.shields.io/badge/LocalStack-3.4.0-000000?style=flat&logo=amazon-aws&logoColor=white)

---

## Sobre o projeto

Pipeline CI/CD completo construído como primeiro projeto de portfólio DevOps. A aplicação é uma API em Flask containerizada com Docker, com três estágios automatizados de entrega disparados a cada `git push` na branch main.

O objetivo foi simular o fluxo real de entrega contínua usado em empresas de tecnologia: nenhum deploy acontece manualmente. Cada alteração no código passa por testes automatizados, build da imagem Docker e verificação do ambiente antes de chegar à etapa de deploy.

Por não ter acesso a cloud com cartão de crédito, a infraestrutura AWS é simulada localmente via LocalStack — o que demonstra o mesmo conceito de integração com serviços cloud independente do ambiente utilizado. A migração para AWS real exigiria apenas substituir o endpoint e as credenciais.

---

## Arquitetura

<p align="center">
  <img width="540" height="675" alt="workflow" src="https://github.com/user-attachments/assets/56b68f40-c7f0-4f8d-a30f-9a148ea018d5" />
</p>

---

## Stack

| Ferramenta | Versão | Uso |
|---|---|---|
| Python | 3.11 | Linguagem da aplicação |
| Flask | 3.1.3 | Framework da API REST |
| Pytest | 9.1.1 | Testes automatizados |
| Docker | 24.x | Containerização da aplicação |
| Docker Compose | 2.x | Orquestração dos serviços |
| GitHub Actions | — | Pipeline CI/CD |
| LocalStack | **3.4.0** | Simulação de serviços AWS (S3) |
| AWS CLI | **1.32.0** | Interação com LocalStack via CLI |

---

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com)
- [Python 3.11+](https://www.python.org/downloads)
- Conta no [GitHub](https://github.com)

---

## Como rodar localmente

**Via Docker Compose (recomendado):**

```bash
git clone https://github.com/eringui/pipeline-cicd-lab
cd pipeline-cicd-lab
docker compose up -d
```

Aguarda ~15 segundos para o LocalStack inicializar, depois acessa:

- API: [http://localhost:5000](http://localhost:5000)
- Health check: [http://localhost:5000/health](http://localhost:5000/health)
- LocalStack: [http://localhost:4566/_localstack/health](http://localhost:4566/_localstack/health)

**Para parar:**

```bash
docker compose down
```

---

**Para desenvolvimento local (sem Docker):**

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\Activate.ps1   # Windows

pip install -r requirements.txt
flask run --host=0.0.0.0 --port=5000
```

---

## Endpoints da API

| Método | Rota | Descrição | Resposta |
|---|---|---|---|
| GET | `/` | Informações do projeto | `{"status": "ok", "project": "Pipeline CI/CD Lab", "author": "Erick Paiva Silva"}` |
| GET | `/health` | Health check da aplicação | `{"status": "healthy"}` |

---

## Rodando os testes

```bash
source venv/bin/activate
pytest -v
```

Resultado esperado:

```
collected 3 items

test_app.py::test_index_retorna_200       PASSED
test_app.py::test_index_retorna_status_ok PASSED
test_app.py::test_health_retorna_healthy  PASSED

3 passed in 0.45s
```

---

## Pipeline CI/CD

O pipeline é composto por três jobs executados em sequência via `needs`. Qualquer falha em qualquer etapa interrompe o fluxo — código quebrado nunca chega ao deploy.

### Job 1 — test
Roda em `ubuntu-latest`. Instala as dependências via `requirements.txt` e executa o pytest. Se qualquer teste falhar, os jobs seguintes são cancelados automaticamente.

### Job 2 — build
Roda em `ubuntu-latest`, depende do `test`. Constrói a imagem `cicd-lab-app`, sobe um container temporário, aguarda 5 segundos, verifica se `/health` retorna 200 via `curl -f`, para e remove o container. Garante que a imagem é válida antes do deploy.

### Job 3 — deploy
Roda em `ubuntu-latest`, depende do `build`. Instala o AWS CLI v1 (1.32.0) e o awscli-local. Sobe o ambiente completo via Docker Compose — aplicação Flask e LocalStack 3.4.0. Cria o bucket S3 simulado, faz upload do artefato via `s3api put-object` e verifica se a aplicação responde corretamente.

---

## Estrutura do projeto

```
pipeline-cicd-lab/
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline GitHub Actions
├── .dockerignore           # Arquivos ignorados pelo Docker
├── .gitignore              # Arquivos ignorados pelo Git
├── app.py                  # Aplicação Flask
├── docker-compose.yml      # Orquestração (app + localstack)
├── Dockerfile              # Containerização da aplicação
├── README.md               # Este arquivo
├── requirements.txt        # Dependências Python
└── test_app.py             # Testes com Pytest
```

---

## Decisões técnicas

**Por que Flask e não Django?**
Flask é uma aplicação mais simples e recomendável para iniciantes, suficiente para demonstrar containerização e CI/CD. Django oferece mais recursos, mas exige conhecimento mais aprofundado.

**Por que LocalStack e não self-hosted runner?**
O self-hosted runner exigia que a pasta do agente (~150MB) ficasse rastreada no repositório, gerando conflito com o limite de espaço do GitHub. O LocalStack roda nos servidores do GitHub e simula os serviços AWS necessários sem depender de infraestrutura local ou conta cloud com cartão.

**Como seria a migração para AWS real?**
Duas mudanças: remover o serviço `localstack` do `docker-compose.yml` e substituir `AWS_ENDPOINT_URL` pelas credenciais reais via GitHub Secrets. O código da aplicação, o Dockerfile e o workflow não mudam nada.

---

## Autor

**Erick Paiva Silva** — estudante de TI, 6° semestre, construindo portfólio DevOps com foco em Cloud Computing e automação de infraestrutura.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/erickpaivasilva/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/eringui)