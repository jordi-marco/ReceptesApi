# 🍳 Receptes API (Backend)

[![Deploy on Railway](https://img.shields.io/badge/Railway-Deployed-blueviolet?style=for-the-badge&logo=railway)](https://la-teva-app.up.railway.app/docs)

> **🌐 URL en viu:** [https://la-teva-app.up.railway.app/docs](https://la-teva-app.up.railway.app/docs)

Aquesta és una API REST i WebSocket construïda amb **FastAPI** per gestionar una aplicació de receptes de cuina.

## 🚀 Tecnologies utilitzades

* **FastAPI**: Framework web d'alt rendiment.
* **SQLAlchemy 2.0**: ORM per a la gestió de la base de dades.
* **PostgreSQL**: Base de dades relacional.
* **Pydantic**: Validació de dades i ús d'àlies (camelCase per al frontend).
* **WebSockets**: Actualitzacions en temps real per a l'app.
* **Railway**: Plataforma de desplegament (Cloud).

## 🛠️ Estructura del Projecte

L'arquitectura és modular per facilitar l'escalabilitat:
- `api/`: Rutes i lògica dels endpoints.
- `core/`: Configuració de la DB i gestor de WebSockets.
- `models/`: Models de taules de SQLAlchemy.
- `schemas/`: Esquemes de validació de Pydantic.

## 📦 Instal·lació i ús local

1. **Clona el repositori:**
   ```bash
   git clone [https://github.com/el-teu-usuari/receptes-backend.git](https://github.com/el-teu-usuari/receptes-backend.git)
   cd receptes-backend

2. **Crea un entorn virtual i actival:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # A Windows: .venv\Scripts\activate

3. **Instal·la les dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Configura les variables d'entorn: Crea un fitxer .env a l'arrel amb la teva URL de Postgres:**
   ```bash
   DATABASE_URL=postgresql+psycopg://usuari:password@host:port/database

5. **Executa l'API:**
   ```bash
   fastapi dev main.py  

## 📑 Endpoints Principals (REST)
| Mètode | Ruta | Descripció |
| :--- | :--- | :--- |
| **GET** | `/receptes/` | Obté la llista de totes les receptes. |
| **POST** | `/receptes/` | Crea una nova recepta. |
| **PUT** | `/receptes/{id}` | Actualitza una recepta existent. |
| **PUT** | `/receptes/{id}/like` | Incrementa el comptador de likes. |
| **DELETE** | `/receptes/{id}` | Elimina una recepta i en retorna les dades. |