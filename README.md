# 🍳 Receptes API (Backend)

[![Deploy on Railway](https://img.shields.io/badge/Railway-Deployed-blueviolet?style=for-the-badge&logo=railway)](https://la-teva-app.up.railway.app/docs)

> **🌐 URL en viu:** [https://receptesapi-production.up.railway.app/docs](https://receptesapi-production.up.railway.app/docs)

Aquesta és una API REST i WebSocket construïda amb **FastAPI** per gestionar una aplicació de receptes de cuina.

## 🚀 Tecnologies utilitzades

* **FastAPI**: Framework web d'alt rendiment.
* **SQLAlchemy 2.0**: ORM per a la gestió de la base de dades.
* **PostgreSQL**: Base de dades relacional.
* **Pydantic**: Validació de dades i ús d'àlies (camelCase per al frontend).
* **WebSockets**: Actualitzacions en temps real per a l'app.
* **Railway**: Plataforma de desplegament (Cloud).

---

## 🛠️ Estructura del Projecte

L'arquitectura és modular per facilitar l'escalabilitat:

* `api/`: Rutes i lògica dels endpoints.
* `core/`: Gestor de WebSockets.
* `models/`: Models de taules de SQLAlchemy.
* `services/`: Serveis de dades, que obenen les dades de la Base de Dades.
* `schemas/`: Esquemes de validació de Pydantic.

---

## 📦 Instal·lació i ús local

1. **Clona el repositori:**

   ```bash
   git clone https://github.com/jordi-marco/ReceptesApi
   cd ReceptesApi

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

---

##  📑 Endpoints Principals (REST)

| Mètode | Ruta | Descripció |
| :--- | :--- | :--- |
| **GET** | `/receptes/` | Obté la llista de totes les receptes. |
| **POST** | `/receptes/` | Crea una nova recepta. |
| **PUT** | `/receptes/{id}` | Actualitza una recepta existent. |
| **PUT** | `/receptes/{id}/like` | Incrementa el comptador de likes. |
| **DELETE** | `/receptes/{id}` | Elimina una recepta i en retorna les dades. |

---

## 📡 WebSockets & Real-Time Updates

A part dels mètodes CRUD tradicionals, l'API inclou un servei de **WebSockets** per sincronitzar la llista de dades en temps real amb els clients connectats.

### Endpoints de WebSocket

* `WS /ws/receptes`: Subscripció a la llista global de receptes.

### Com funciona?

1. **Connexió:** El client obre una connexió persistent.
2. **Escolta:** El servidor manté el client en una llista de "connexions actives".
3. **Broadcast:** Cada vegada que es realitza una operació d'escriptura (Create, Update o Delete) a través de l'API REST, el servidor automàticament envia un JSON amb la llista actualitzada de tots els objectes a tots els clients connectats.

### Exemple de Payload (JSON)

En qualsevol canvi, els clients reben el llistat sencer d'objectes:

```json
[
   {
      "id": 5,
      "nom": "Truita de Patates",
      "descripcio": "Talla les patates (i opcionalment, la ceba) fregir suaument durant 25-30 minuts. Bat els ous. Afegeix sal al teu gust. Barreja les patates i els ous batuts i deixa reposar almenys 2 hores. Fregeix la barreja deixant que qualli i fent la volta amb un plat o tapa",
      "minuts": 45,
      "ingredients": [
         "Patates",
         "Ous",
         "Oli",
         "Sal"
      ],
      "likes": 41,
      "urlImatge": "http://elpetitchef.com/sites/default/files/2021-05/presentacion_1.jpg"
   },
   {
      "id": 6,
      "nom": "Dieta sindrome de pica",
      "descripcio": "dieta para estómagos resistentes ",
      "minuts": 2,
      "ingredients": [
         "Clavos",
         " cubiertos y vasos"
      ],
      "likes": 0,
      "urlImatge": null
   }
  ]
