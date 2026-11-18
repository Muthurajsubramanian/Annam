# Annam Restaurant — Backend (Django + Django REST Framework)

A REST API backend for your existing HTML/CSS/JS frontend. It does **not**
replace your frontend files — your `index.html`, `about.html`, etc. stay
exactly as they are, served however you're serving them now (e.g. VS Code
Live Server). This backend just gives them a real API to talk to.

## What it covers

| App        | Handles |
|------------|---------|
| `accounts` | Register, login, logout, get-current-user (token-based auth) — powers `login.html` |
| `menu`     | Categories + menu items — powers the Offer page tabs and Home page "Popular Food Items" |
| `contact`  | Stores messages submitted from the Contact page form |
| `orders`   | Cart (add/update/remove items) and checkout → creates an Order — powers the "Cart (1)" badge on the Offer page |

All data is editable afterwards through Django's built-in admin panel at
`/admin/` — no need to touch the code to change a price or read a contact
message.

## 1. Install

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Set up the database

```bash
python manage.py makemigrations accounts menu contact orders
python manage.py migrate
python manage.py loaddata menu/fixtures/menu_data.json   # seeds categories + menu items
python manage.py createsuperuser                          # for the /admin/ panel
```

## 3. Run it

```bash
python manage.py runserver
```

The API is now live at `http://127.0.0.1:8000/`. Django admin is at
`http://127.0.0.1:8000/admin/`.

## 4. Run your frontend alongside it

Keep serving your frontend with VS Code's **Live Server** (or any static
server) — just not by double-clicking the HTML file, since `fetch()` calls
to the API need a real origin (`http://127.0.0.1:5500`, not `file://`).

`settings.py` already allows `http://127.0.0.1:5500` and
`http://localhost:5500` (Live Server's default ports) to call the API via
CORS. If Live Server picks a different port for you, add it to
`CORS_ALLOWED_ORIGINS` in `annam/settings.py`.

## API reference

### Auth
| Method | Endpoint | Body | Notes |
|---|---|---|---|
| POST | `/api/auth/register/` | `{ username, email, password }` | Returns `{ token, user }` |
| POST | `/api/auth/login/` | `{ email, password }` | Returns `{ token, user }` |
| POST | `/api/auth/logout/` | — | Requires `Authorization: Token <token>` header |
| GET | `/api/auth/me/` | — | Requires auth header |

### Menu
| Method | Endpoint | Notes |
|---|---|---|
| GET | `/api/menu/categories/` | All categories with nested items (Offer page tabs) |
| GET | `/api/menu/featured/` | Items flagged `is_featured` (Home page food cards) |

### Contact
| Method | Endpoint | Body |
|---|---|---|
| POST | `/api/contact/` | `{ full_name, email, phone, subject, message }` |

### Orders (all require the `Authorization: Token <token>` header)
| Method | Endpoint | Body | Notes |
|---|---|---|---|
| GET | `/api/orders/cart/` | — | Current cart |
| POST | `/api/orders/cart/add/` | `{ menu_item, quantity }` | Adds/increments item |
| PATCH | `/api/orders/cart/items/<id>/` | `{ quantity }` | Update quantity |
| DELETE | `/api/orders/cart/items/<id>/` | — | Remove item |
| POST | `/api/orders/checkout/` | `{ delivery_address, phone }` | Creates an Order, empties cart |
| GET | `/api/orders/` | — | Order history |

## Wiring this into your existing frontend

Your uploaded HTML files don't call the API yet — they're plain forms/
buttons right now. I've prepared a matching `frontend-integration.js` script
below (see the next message) that you can drop into your `login.html`,
`contact.html`, and `offer.html` to connect the buttons/forms to these
endpoints. It handles: storing the login token, submitting the contact
form, and adding items to the cart + updating the floating cart badge.

## Moving beyond SQLite

SQLite (the default here) is perfect for development. For production,
swap the `DATABASES` block in `annam/settings.py` for Postgres or MySQL
and set `DEBUG = False` plus a real `DJANGO_SECRET_KEY` environment
variable.
