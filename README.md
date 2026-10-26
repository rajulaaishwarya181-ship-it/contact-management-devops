# Contact Management System — DevOps Case Study

A beginner-friendly CRUD web application built with Flask and SQLite, containerized with Docker, tested through GitHub Actions, and deployable to Render.

## Features
- Add, view, edit, and delete contacts
- Search by name, phone, or email
- SQLite storage
- Health endpoint at `/health`
- Automated tests and Docker build in GitHub Actions

## Run locally on Windows
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

If PowerShell blocks activation, run this in the same PowerShell window and retry:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Run tests
```powershell
python -m unittest discover -s tests -v
```

## Run with Docker
Start Docker Desktop first, then:
```powershell
docker build -t contact-manager .
docker run --rm -p 5000:5000 -e DATABASE_PATH=/app/instance/contacts.db -v contact-data:/app/instance contact-manager
```
Open http://localhost:5000

## GitHub
Create an empty GitHub repository, then run these commands from the project folder:
```powershell
git init
git add .
git commit -m "Initial Contact Management System"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/contact-management-devops.git
git push -u origin main
```
Replace the URL with your actual repository URL. Git must be installed.

## Render deployment
1. Push the project to GitHub.
2. In Render, create a **New Web Service** and connect the repository.
3. Choose **Docker** as the runtime.
4. Set health check path to `/health`.
5. For persistent SQLite data, add a persistent disk mounted at `/var/data`.
6. Set environment variable `DATABASE_PATH` to `/var/data/contacts.db`.
7. Set `SECRET_KEY` to a long random secret.
8. Deploy and test the service URL.

Note: persistent disks may not be available on every free hosting plan. If your plan does not support one, use a managed PostgreSQL database instead; the default container filesystem may be ephemeral.

## DevOps concepts demonstrated
- Version control: Git and GitHub
- CI: automated tests on push and pull requests
- Containerization: Docker
- CD/deployment: Render connected to GitHub
- Health check: `/health`
- Persistence: mounted data directory or managed database
