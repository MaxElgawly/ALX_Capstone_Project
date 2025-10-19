Inventory Management API (Django + DRF)
Setup (local):

python -m venv venv
source venv/bin/activate # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env and edit SECRET_KEY, DEBUG, DB settings if needed
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
API endpoints:

/api/items/ (GET, POST)
/api/items/{id}/ (GET, PUT, PATCH, DELETE) -- restricted to owner for write
/api/items/{id}/history/ (GET) -- inventory change history
/api/categories/ (if enabled)
/api/auth/token/ (JWT token obtain)
/ (UI pages) - item list, detail, login/register
Notes:

Inventory quantity changes are logged in InventoryChangeLog
Filtering, search, pagination supported
