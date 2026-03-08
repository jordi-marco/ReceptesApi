# 🍳 Receptes API (Backend)

<!-- 
[![Deploy on Railway](https://img.shields.io/badge/Railway-Deployed-blueviolet?style=for-the-badge&logo=railway)](https://la-teva-app.up.railway.app/docs)

> **🌐 URL en viu:** [https://receptesapi-production.up.railway.app/docs](https://receptesapi-production.up.railway.app/docs)
-->

Aquesta és una API REST i WebSocket construïda amb **FastAPI** per gestionar una aplicació de receptes de cuina.

## 🚀 Tecnologies utilitzades

* **FastAPI**: Framework web d'alt rendiment.
* **SQLAlchemy 2.0**: ORM per a la gestió de la base de dades.
* **PostgreSQL**: Base de dades relacional.
* **Pydantic**: Validació de dades i ús d'àlies (camelCase per al frontend).
* **WebSockets**: Actualitzacions en temps real per a l'app.
<!-- * **Railway**: Plataforma de desplegament (Cloud). -->

---

## 🛠️ Estructura del Projecte

L'arquitectura és modular per facilitar l'escalabilitat:

* `api/`: Rutes i lògica dels endpoints.
* `core/`: Gestor de WebSockets.
* `models/`: Models de taules de SQLAlchemy.
* `services/`: Serveis de dades, que obtenen les dades de la Base de Dades.
* `schemas/`: Esquemes de validació de Pydantic.

---

## 📦 Instal·lació i ús local

1. **Clonar el repositori:**

   ```bash
   git clone https://github.com/jordi-marco/ReceptesApi
   cd ReceptesApi
   ```

2. **Crear un entorn virtual i activar-ho:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # A Windows: .venv\Scripts\activate
   ```

3. **Instal·lar les dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar les variables d'entorn:**

   Crear un fitxer `.env` a l'arrel del projecte basant-se en el fitxer `.env.example`. En aquest cas, la `DB_HOST` haurà d'apuntar al host on estigui el PostgreSQL (normalment localhost). Modificar les variables amb els valors de la ip del host de la base de dades (localhost si és local) i les seves credencials:

   ```bash
   # Exemple de fitxer .env per a la configuració de la base de dades
   # Aquest fitxer ha de ser renombrat a .env i editat amb els valors 
   # de la ip del host de la base de dades i les seves credencials

   # Fer servir 
   #    'db': per a Docker (db és el nom del servei de la base de dades al docker-compose)
   #    'localhost': per a base de dades local
   #    ip de la màquina on està la base de dades: per a base de dades remota
   DB_HOST= db | localhost | ip_address
   DB_PORT=5432

   # Credencials de la base de dades
   DB_USER=user
   DB_PASSWORD=userpassword
   DB_NAME=databasename

   # URL de connexió construïda amb les variables anteriors
   DATABASE_URL=postgresql+psycopg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
   ```

5. **Executar l'API:**

   ```bash
   fastapi dev main.py 
   ```

6. **Comprovar el funcionament:**

   🌐 URL:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📦 Instruccions de Desplegament a un servidor

### Opció A: Desplegament amb Docker (Recomanat)

Aquest mètode utilitza **Docker Compose** per aixecar l'API i la base de dades en contenidors aïllats.

1. **Clonar el repositori:**

   ```bash
   git clone https://github.com/jordi-marco/ReceptesApi
   cd ReceptesApi
   ```

2. **Configurar les variables d'entorn:**

   Crea un fitxer `.env` a l'arrel del projecte basant-se en el fitxer `.env.example`. En aquest cas, utilitzar `db` com a valor de la variable `DB_HOST`. Modificar els valors de les credencials:

   ```bash
   # Exemple de fitxer .env per a la configuració de la base de dades
   # Aquest fitxer ha de ser renombrat a .env i editat amb els valors 
   # de la ip del host de la base de dades i les seves credencials

   # Fer servir 
   #    'db': per a Docker (db és el nom del servei de la base de dades al docker-compose)
   #    'localhost': per a base de dades local
   #    ip de la màquina on està la base de dades: per a base de dades remota
   DB_HOST=db
   DB_PORT=5432

   # Credencials de la base de dades
   DB_USER=user
   DB_PASSWORD=userpassword
   DB_NAME=databasename

   # URL de connexió construïda amb les variables anteriors
   DATABASE_URL=postgresql+psycopg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
   ```

3. **Executar:**

   Un cop configurat el fitxer .env, executa la següent comanda:

   ``` bash
   docker-compose up -d --build
   ```

   L'API estarà disponible internament al port 8000.

### Opció B: Desplegament natiu (Sense Docker)

Si el servidor no disposa de Docker, segueix aquests passos:

1. **Clonar el repositori:**

   ```bash
   git clone https://github.com/jordi-marco/ReceptesApi
   cd ReceptesApi
   ```

2. **Crear un entorn virtual i activar-ho:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # A Windows: .venv\Scripts\activate
   ```

3. **Instal·lar les dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar les variables d'entorn:**

   Crear un fitxer `.env` a l'arrel del projecte basant-se en el fitxer `.env.example`. En aquest cas, la `DB_HOST` haurà d'apuntar al host on estigui el PostgreSQL (normalment localhost). Modificar les variables amb els valors de la ip del host de la base de dades (localhost si és local) i les seves credencials:

   ```bash
   # Exemple de fitxer .env per a la configuració de la base de dades
   # Aquest fitxer ha de ser renombrat a .env i editat amb els valors 
   # de la ip del host de la base de dades i les seves credencials

   # Fer servir 
   #    'db': per a Docker (db és el nom del servei de la base de dades al docker-compose)
   #    'localhost': per a base de dades local
   #    ip de la màquina on està la base de dades: per a base de dades remota
   DB_HOST= db | localhost | ip_address
   DB_PORT=5432

   # Credencials de la base de dades
   DB_USER=user
   DB_PASSWORD=userpassword
   DB_NAME=databasename

   # URL de connexió construïda amb les variables anteriors
   DATABASE_URL=postgresql+psycopg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
   ```

5. **Execució del servidor**

   Executa l'API utilitzant Uvicorn:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## 🛠️ Notes per a l'Administrador del Servidor

* **Reverse Proxy:** L'API està configurada per escoltar al port **8000**. Es recomana l'ús d'un proxy invers (com Nginx o Traefik) per gestionar la terminació TLS/SSL (HTTPS) i dirigir el tràfic al subdomini corresponent.
* **Seguretat:** El fitxer `.env` real ha de ser generat al servidor. Les credencials de la base de dades es poden triar lliurement; l'aplicació les llegirà mitjançant les variables d'entorn definides.
* **Persistència:** Si s'utilitza Docker, s'ha definit un volum anomenat `postgres_data` al fitxer `docker-compose.yml` per assegurar que les dades no es perdin en reiniciar els contenidors.

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
  ```
