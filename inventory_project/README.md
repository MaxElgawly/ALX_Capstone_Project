Inventory Management API (Django + DRF)
--------------------------------------

Setup (local):

1. python -m venv venv
2. source venv/bin/activate   # on Windows: venv\Scripts\activate
3. pip install -r requirements.txt
4. cp .env.example .env and edit SECRET_KEY, DEBUG, DB settings if needed
5. python manage.py migrate
6. python manage.py createsuperuser
7. python manage.py runserver

API endpoints:
- /api/items/             (GET, POST)
- /api/items/{id}/        (GET, PUT, PATCH, DELETE) -- restricted to owner for write
- /api/items/{id}/history/ (GET) -- inventory change history
- /api/categories/        (if enabled)
- /api/auth/token/        (JWT token obtain)
- / (UI pages) - item list, detail, login/register

Notes:
- Inventory quantity changes are logged in InventoryChangeLog
- Filtering, search, pagination supported
