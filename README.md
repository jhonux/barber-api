<div align="center">

# 💈 **BarberAPI**

API RESTful desenvolvida em **Python + FastAPI** para gerenciamento e agendamento de uma **barbearia**.  
Projeto criado para **portfólio**, aplicando boas práticas de **arquitetura**, **segurança** e **ambiente de desenvolvimento**.

---

### 🧰 **Tecnologias Principais**

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-High%20Performance-brightgreen?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-orange?logo=python)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-green?logo=pydantic)
![JWT](https://img.shields.io/badge/JWT-Auth-black?logo=jsonwebtokens)

</div>

---

## 🚧 **Status do Projeto**

> 🔄 **Em desenvolvimento ativo**
>
> ✅ **Fase 1 (concluída):** Base segura da API, autenticação, hashing e proteção de endpoints.  
> 🚀 **Próximas fases:** Implementação da lógica de agendamento e interface de administração.

---

## ✨ **Funcionalidades (Fase 1 Concluída)**

A base da aplicação está construída com foco total em **segurança** e **escalabilidade**:

- 🔐 **Autenticação de Usuários com JWT:**  
  Sistema completo de cadastro e login com geração de tokens de acesso protegidos.

- 🔒 **Hashing Seguro de Senhas:**  
  As senhas são criptografadas com **bcrypt**, garantindo sigilo total.

- 🧱 **Endpoints Protegidos:**  
  Apenas usuários autenticados podem criar e manipular recursos (como serviços).

- 🧾 **Validação de Dados com Pydantic:**  
  Todos os dados são validados antes de entrar na API, evitando inconsistências.

---

## 🛠️ **Tecnologias Utilizadas**

| **Ferramenta**              | **Descrição**                                                                                  |
|-----------------------------|------------------------------------------------------------------------------------------------|
| **Python 3.11+**            | Linguagem de programação principal.                                                           |
| **FastAPI**                 | Framework web de alta performance para a construção da API.                                   |
| **PostgreSQL**              | Banco de dados relacional para armazenamento dos dados.                                       |
| **Docker & Docker Compose** | Para criar um ambiente de desenvolvimento isolado e reproduzível, gerenciando o serviço do banco de dados. |
| **SQLAlchemy**              | ORM (Object-Relational Mapper) para interagir com o banco de dados usando código Python.       |
| **Pydantic**                | Para validação e serialização de dados, garantindo a integridade da API.                      |
| **Passlib & python-jose**   | Bibliotecas para hashing de senhas e gerenciamento de Tokens JWT.                             |

---

## 🚀 **Como Executar o Projeto Localmente**

### 🔧 Pré-requisitos

- **Python 3.11+**
- **Docker**
- **Git**

---

### 🪜 **Passos de Instalação**

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/jhonux/barber-api.git
   cd barber-api

2. **Crie e ative o ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt

   
4. **Configure as variáveis de ambiente**:
    Crie o arquivo .env (ou copie de .env.example) e adicione:
    ```bash
    SECRET_KEY="sua_chave_secreta_gerada_aqui"

5. **Inicie o banco de dados com Docker:**
    ```bash
    docker-compose up -d

6. **Execute a API:**
    ```bash
    uvicorn main:app --reload

📡 Documentação da API

A documentação interativa é gerada automaticamente pelo FastAPI:

🧭 Swagger UI: http://127.0.0.1:8000/docs

📘 ReDoc: http://127.0.0.1:8000/redoc

🔑 Principais Endpoints (Fase 1)
| Método | Endpoint     | Descrição                                         | Autenticação |
| ------ | ------------ | ------------------------------------------------- | ------------ |
| POST   | `/users/`    | Cria um novo usuário (dono da barbearia).         | ❌            |
| POST   | `/token`     | Realiza o login e retorna um token de acesso JWT. | ❌            |
| GET    | `/users/me/` | Retorna os dados do usuário logado.               | ✅            |
| POST   | `/services/` | Cria um novo serviço oferecido pela barbearia.    | ✅            |

 Fase 1: Estrutura segura da API (concluída)

 Fase 2: Ferramenta Interna

 CRUD completo para Services (Update e Delete)

 CRUD para Availability (definição de horários de trabalho)

 CRUD para Appointments (agendamento manual de clientes)

 Fase 3: Abertura para Clientes

 Endpoint público para consulta de horários disponíveis

 Endpoint público para agendamentos por clientes

👤 Contato

Jonatas Pereira de Souza
🔗 LinkedIn: [Jonatas Pereira de Souza](https://www.linkedin.com/in/jon-souza)
💻 GitHub: [JhonUx](https://github.com/jhonux)


<div align="center"> Feito com ❤️ e ☕ por <b>Jonatas Souza</b> <br> <sub>© 2025 BarberAPI. Todos os direitos reservados.</sub> </div> 




