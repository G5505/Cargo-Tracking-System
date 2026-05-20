# Cargo-Tracking-System

A web-based cargo tracking system developed using Flask, SQLite, HTML, CSS, and JavaScript.

## Features

- Track shipments using Tracking ID
- View shipment history
- Add new shipments
- Update shipment status
- Delete shipments
- Dashboard statistics
- RESTful API support
- Admin panel for shipment management

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

## System Architecture

The system follows a layered architecture:

- Frontend Layer
- Backend API Layer
- Database Layer

## APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/track/<tracking_id> | Get shipment details |
| GET | /api/history/<tracking_id> | Get shipment history |
| POST | /api/add | Add new shipment |
| PUT | /api/update/<tracking_id> | Update shipment status |
| DELETE | /api/delete/<tracking_id> | Delete shipment |
| GET | /api/dashboard | Get dashboard statistics |

## Project Structure

```text
Cargo-Tracking-System/
│
├── app.py
├── database.py
├── models.py
├── cargo.db
│
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── login.html
│
├── static/
│   └── style.css
│
└── README.md
