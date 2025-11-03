# 🧩 2FA Microservice — Autenticação em Duas Etapas com FastAPI e MongoDB

Este projeto é um **microserviço de autenticação em duas etapas (2FA)** desenvolvido com **FastAPI** e **MongoDB**.  
Ele permite que usuários configurem a autenticação com aplicativos como **Google Authenticator**, **Microsoft Authenticator**, entre outros.  
O serviço também gera **códigos de recuperação** e permite **regenerar** ou **validar** o 2FA.

---

## 🚀 Funcionalidades

- 🔐 **Criação de autenticação 2FA (TOTP)**  
  Gera um QR Code e um *secret key* compatível com apps autenticadores.

- 🧾 **Códigos de recuperação**  
  O sistema gera 5 códigos únicos de recuperação, utilizados caso o usuário perca o acesso ao autenticador.

- 🔁 **Validação de códigos 2FA**  
  Permite verificar o código TOTP inserido pelo usuário em tempo real.

- ♻️ **Recuperação e regeneração**  
  Caso o usuário perca o acesso, ele pode validar um código de recuperação e gerar um novo 2FA.

- 💾 **Integração com MongoDB**  
  Armazena usuários, secrets e códigos de recuperação criptografados com segurança.

- 🧱 **Estrutura modular**  
  Separação clara entre camadas de:
  - `models/` → modelos de dados  
  - `schemas/` → validação e documentação  
  - `services/` → regras de negócio  
  - `db/` → integração com o banco  
  - `core/` → dependências e segurança  
  - `api/v1/` → rotas da API  

---

## 🧠 Tecnologias Utilizadas

| Tecnologia | Função |
|-------------|--------|
| **FastAPI** | Framework principal da API |
| **Motor** | Driver assíncrono do MongoDB |
| **PyOTP** | Geração e validação de códigos TOTP |
| **QRCode** | Criação dos QR Codes do autenticador |
| **Pydantic** | Validação dos dados |
| **Uvicorn** | Servidor ASGI |
| **Docker** | Empacotamento do microserviço |

---

## 📁 Estrutura de Pastas

```

2fa_service/
├── core/
│   ├── database.py         # Conexão com o MongoDB
│   ├── Security.py         # Geração de secrets, QR e recovery codes
│   └── deps.py             # Dependências do FastAPI
├── db/
│   └── Crud.py             # Operações CRUD no banco
├── models/
│   └── user_model.py       # Modelo do usuário
├── schemas/
│   └── user_schema.py      # Schemas do FastAPI
├── services/
│   └── User_service.py     # Lógica de negócio do usuário e 2FA
├── api/v1/endpoints/
│   └── user_2fa.py         # Rotas públicas da API
├── config.py               # Variáveis de ambiente
├── main.py                 # Ponto de entrada da aplicação
├── Dockerfile              # Imagem Docker
└── requirements.txt        # Dependências do projeto

````

---

## ⚙️ Configuração do Ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/mateushlsilva/2fa_service.git
cd 2fa_service
````

### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` (ou configure diretamente no `config.py`):

```
DATABASE_URL=mongodb://localhost:27017/2fa
ENTERPRISE=MinhaEmpresa
```

---

## ▶️ Executar o Servidor

```bash
uvicorn main:app --reload
```

Acesse em:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 Endpoints Principais

### 🔸 Criar 2FA

`POST /2fa/setup`

**Body:**

```json
{
  "identifier": "usuario123"
}
```

**Retorno:**

```json
{
  "qrcode": "base64encodedimage",
  "media_type": "image/png",
  "recovery": ["code1", "code2", "code3", "code4", "code5"]
}
```

---

### 🔸 Verificar código 2FA

`GET /2fa/verify?identifier=usuario123&code=123456`

**Retorno:**

```json
{
  "status": "success"
}
```

---

### 🔸 Validar código de recuperação

`PATCH /2fa/recovery/generate`

**Body:**

```json
{
  "identifier": "usuario123",
  "code": "meu_codigo_de_recuperacao"
}
```

**Retorno:**

```json
{
  "status": "success"
}
```

---

## 🐳 Rodar com Docker

### 1. Build da imagem

```bash
docker build -t 2faservice .
```

### 2. Executar o container

```bash
docker run --name 2fa \
  -e DATABASE_URL=mongodb://host.docker.internal:27017/2fa \
  -e ENTERPRISE=MinhaEmpresa \
  -p 8000:8000 2faservice
```

---


## 🧩 Exemplos de Integração

Você pode integrar este microserviço com:

* Portais corporativos internos
* Sistemas de autenticação personalizados
* APIs REST que exigem 2FA
* Front-ends em React, Angular, Vue etc.

---

## 🧰 Requisitos

* Python 3.10+
* MongoDB 6+
* Docker (opcional)
* FastAPI e Motor instalados

---

## 🧑‍💻 Autor

**Mateus Silva**
Desenvolvedor Full Stack | Especialista em APIs e Microsserviços
📍 São José dos Campos - SP

---

## 📝 Licença

Este projeto está sob a licença MIT — sinta-se livre para utilizar, modificar e distribuir.

