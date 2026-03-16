# ReadTrack — Project Overview

## Description

ReadTrack is a comprehensive book management system that enables users to track their reading progress, store notes and files, and manage detailed information about books and authors. With a modern React interface, a secure Flask backend, and a structured data model, ReadTrack provides an efficient and intuitive environment for organizing a personal reading library.

## Features

- **Reading Progress Tracking** — Track pages and chapters read per book with visual progress bars.
- **Notes & File Storage** — Add notes tied to specific pages and upload files (PDF, images, documents) per book.
- **Book Management** — Full CRUD for books with fields for title, author, genre, publisher, ISBN, rating, and status.
- **Author Management** — Create and manage author profiles with biographies and linked publications.
- **JWT Authentication** — Secure user registration and login with access/refresh token flow.
- **Responsive UI** — Clean, modern React interface that works across desktop and mobile.
- **RESTful API** — Well-structured JSON API with consistent response envelopes.

## Tech Stack

| Layer    | Technology                                    |
| -------- | --------------------------------------------- |
| Frontend | React 19, Vite, Axios, React Router           |
| Backend  | Flask 3, Flask-SQLAlchemy, Flask-JWT-Extended |
| Database | SQLite                                        |
| Testing  | pytest, pytest-flask                          |
| Auth     | JWT (access + refresh tokens)                 |
