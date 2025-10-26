# 💈 BarberAPI

Uma **API RESTful robusta** desenvolvida em **Python + FastAPI**, projetada para servir como **backend para um sistema de gerenciamento interno de barbearias**.  
Este projeto aplica **boas práticas de arquitetura, segurança, testes, migrações e ambiente de desenvolvimento**.

---

## 🚀 Status do Projeto

✅ **Backend Concluído! (API para gestão interna)**  

A API backend principal para **gerenciamento interno da barbearia** está **finalizada, testada e pronta para deploy**.  
A interface **frontend (Web/Mobile)** será desenvolvida em um projeto separado.

---

## ✨ Funcionalidades Principais (Backend)

A API oferece um conjunto completo de funcionalidades para a gestão interna da barbearia:

- 🔐 **Autenticação Segura:** Sistema completo de cadastro e login de usuários com **Tokens JWT** e **hashing de senhas (bcrypt)**.  
- 🧱 **Endpoints Protegidos:** Rotas de gestão acessíveis apenas a **usuários autenticados**.  
- 🧾 **Validação de Dados:** Integridade garantida através do **Pydantic**.  
- 💼 **Gestão de Serviços (CRUD Completo):** Criação, visualização, atualização e remoção dos serviços oferecidos.  
- 📅 **Gestão de Disponibilidade:** Definição e remoção dos horários de trabalho do profissional.  
- ✍️ **Gestão de Agendamentos Manuais:** Criação, visualização e remoção de agendamentos para clientes.  
- 🌐 **Listagem Pública de Serviços:** Endpoint público para consulta do menu de serviços.  
- 🔄 **Migrações de Banco de Dados:** Estrutura versionada e gerenciada com **Alembic**.  
- ✅ **Testes Automatizados:** Cobertura robusta com **Pytest**.  
- ⚙️ **Pronto para Produção:** Configuração otimizada para **Gunicorn (via WSL/Linux)** e uso de **variáveis de ambiente (.env)**.  

---

## 🛠️ Tecnologias Utilizadas

| Ferramenta | Descrição |
|-------------|------------|
| **Python 3.11+** | Linguagem de programação principal. |
| **FastAPI** | Framework web de alta performance para a construção da API. |
| **PostgreSQL** | Banco de dados relacional (gerenciado via Docker). |
| **Docker & Docker Compose** | Para criar um ambiente de desenvolvimento isolado e reproduzível. |
| **SQLAlchemy** | ORM para interagir com o banco de dados. |
| **Alembic** | Ferramenta para gerenciar migrações do schema do banco de dados. |
| **Pydantic** | Para validação e serialização de dados. |
| **Passlib & python-jose** | Para hashing de senhas (bcrypt) e gerenciamento de Tokens JWT. |
| **Pytest & httpx** | Para escrita e execução de testes automatizados da API. |
| **Gunicorn & Uvicorn** | Servidor ASGI para rodar a aplicação em produção (recomendado via WSL/Linux). |
| **python-dotenv** | Para carregar variáveis de ambiente de um arquivo `.env` em desenvolvimento. |

---

## 🚀 Como Executar o Projeto Localmente

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
    uvicorn app.main:app --reload

📡 Documentação da API

A documentação interativa é gerada automaticamente pelo FastAPI:

🧭 Swagger UI: http://127.0.0.1:8000/docs

📘 ReDoc: http://127.0.0.1:8000/redoc

## 🔑 Endpoints Implementados

| Método | Endpoint                     | Descrição                                          | Status |
|:--------|:------------------------------|:---------------------------------------------------|:-------:|
| **POST**   | `/users/`                     | Cria um novo usuário (dono da barbearia).           | ❌ |
| **POST**   | `/token`                      | Realiza o login e retorna um token de acesso JWT.   | ❌ |
| **GET**    | `/users/me/`                  | Retorna os dados do usuário logado.                 | ✅ |
| **GET**    | `/services/public/`           | Lista todos os serviços (público).                  | ❌ |
| **POST**   | `/services/`                  | Cria um novo serviço.                               | ✅ |
| **GET**    | `/services/`                  | Lista todos os serviços (requer autenticação).      | ✅ |
| **PUT**    | `/services/{service_id}`      | Atualiza um serviço existente.                      | ✅ |
| **DELETE** | `/services/{service_id}`      | Remove um serviço existente.                        | ✅ |
| **POST**   | `/availability/`              | Cria um novo horário de disponibilidade.            | ✅ |
| **GET**    | `/availability/me/`           | Lista os horários de disponibilidade do usuário.    | ✅ |
| **DELETE** | `/availability/{avail_id}`    | Remove um horário de disponibilidade.               | ✅ |
| **POST**   | `/appointments/`              | Cria um novo agendamento (manual).                  | ✅ |
| **GET**    | `/appointments/me/`           | Lista os agendamentos do usuário.                   | ✅ |
| **DELETE** | `/appointments/{appt_id}`     | Remove um agendamento.                              | ✅ |


## 🎯 Possíveis Features Futuras

Embora a funcionalidade principal para gestão interna esteja concluída, o projeto pode ser estendido com novas melhorias e integrações:

### 💼 Gestão de Conta
- Implementar fluxo de **"Esqueci a Senha"** (geração de token de reset e envio de e-mail).  
- Implementar **endpoint para alteração de senha** pelo usuário logado.

### 🔔 Notificações
- Implementar **filas assíncronas** (ex: *Celery + Redis/RabbitMQ*) para envio de notificações, como lembretes de agendamento por **e-mail ou SMS**.

### ☁️ Deploy e Operações
- **Deploy da API na nuvem** (ex: Heroku, Render, AWS).  
- Configurar **pipeline CI/CD** (ex: GitHub Actions) para automatizar testes e deploy contínuo.

---

## 📄 Licença

Este projeto é de **código aberto** e está licenciado sob os termos da **Licença MIT**.  
Sinta-se à vontade para usar, modificar e distribuir o código para qualquer finalidade, **comercial ou não comercial**.

---

## 👤 Contato

**Jonatas Pereira de Souza**  

🔗 [LinkedIn: Jonatas Pereira de Souza](https://www.linkedin.com/in/jon-souza)  
💻 [GitHub: JhonUx](https://github.com/jhonux)

---

<p align="center">Feito com ❤️ e ☕ por <b>Jonatas Souza</b></p>  
<p align="center"><sub>© 2025 BarberAPI. Todos os direitos reservados.</sub></p>




