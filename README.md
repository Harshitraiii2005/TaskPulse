
# TaskPulse – 3-Tier Task Management Application
#visit: https://taskpulse-production-0489.up.railway.app/

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/) 
[![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey?logo=flask)](https://flask.palletsprojects.com/) 
[![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker&logoColor=white)](https://www.docker.com/) 
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Cluster-blue?logo=kubernetes&logoColor=white)](https://kubernetes.io/) 
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red?logo=jenkins&logoColor=white)](https://www.jenkins.io/) 
[![ArgoCD](https://img.shields.io/badge/ArgoCD-Deployment-red?logo=argo&logoColor=white)](https://argo-cd.readthedocs.io/) 
[![Railway](https://img.shields.io/badge/Railway-Cloud-blue?logo=railway&logoColor=white)](https://railway.app/) 
[![NeonDB](https://img.shields.io/badge/Neon-Database-purple?logo=postgresql&logoColor=white)](https://neon.tech/) 
[![Notifications](https://img.shields.io/badge/Notifications-Email-yellow?logo=gmail&logoColor=white)]()

---

## Overview

**TaskPulse** is a **3-tier task management web application** with:

- **Frontend:** User-friendly Flask templates.
- **Backend:** Python Flask APIs.
- **Database:** Neon (serverless PostgreSQL).
- **Notifications:** Email alerts on task creation and due dates.
- **Deployment:** Dockerized with Kubernetes, CI/CD via Jenkins & ArgoCD, hosted on EC2.

**Key Features:**

- User signup and task assignment.
- Add, view, and complete tasks.
- Automatic email notifications for task creation and upcoming due dates.
- Scalable, modular architecture.

---

## Architecture

```

+----------------+      +----------------+      +----------------+
|   Frontend     | ---> |   Backend API  | ---> |   Neon DB      |
|  (Flask UI)    |      | (Flask + APIs)|      | PostgreSQL     |
+----------------+      +----------------+      +----------------+
|
v
Notifications (Email)

````

- **Deployment:** Dockerized application running on Kubernetes.
- **CI/CD:** Jenkins triggers builds → ArgoCD deploys to Railway.

---

## Screenshots

**Main App UI:**

![TaskPulse UI](https://github.com/user-attachments/assets/ac350ef3-a289-42fb-ab57-5285958db03e)

**Jenkins Pipeline:**

![Jenkins CI/CD](https://github.com/user-attachments/assets/29fc5a4a-e270-49f9-85b4-a70f7e6082a1)

**ArgoCD Deployment:**

![ArgoCD](https://github.com/user-attachments/assets/33ae864e-cea3-4f68-ac05-a810641c5052)

---

## Installation / Local Setup

1. Clone the repository:

```bash
git clone https://github.com/Harshitraiii2005/TaskPulse.git
cd TaskPulse
````

2. Create & activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables (`.env` or Railway service variables):

```env
DATABASE_URL=<your_neon_database_url>
EMAIL_ADDRESS=<your_email>
EMAIL_APP_PASSWORD=<your_email_app_password>
SECRET_KEY=<your_secret_key>
```

5. Run backend locally:

```bash
python backend/app.py
```

6. Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Deployment

* **Railway:** Live deployment hosted on Railway.
* **CI/CD:** Jenkins pipeline builds Docker images → ArgoCD deploys to Kubernetes.
* Kubernetes manifests available in `deployment/` folder.

---

## Notifications

* **Task Created:** Email sent to user with task details.
* **Task Due Reminder:** Email alert when a task is approaching its due date.

---

## Tech Stack

| Layer         | Technology                  |
| ------------- | --------------------------- |
| Frontend      | Flask, HTML, CSS, Bootstrap |
| Backend       | Python, Flask, psycopg2     |
| Database      | Neon (PostgreSQL)           |
| CI/CD         | Jenkins, ArgoCD             |
| Deployment    | Docker, Kubernetes, Railway |
| Notifications | SMTP Email                  |

---

## Contributing

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'Add some feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Open a Pull Request.

---

## License

MIT License © 2026 Harshit Rai

---

**Live App:** [TaskPulse on Railway](https://taskpulse-production-0489.up.railway.app)

```

