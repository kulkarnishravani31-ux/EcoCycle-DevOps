# EcoCycle — College Demonstration Guide

## 1. Problem statement
Electronic waste is often discarded without a convenient collection workflow. EcoCycle provides a simple way for users to request responsible e-waste pickup and for administrators to manage collection status.

## 2. Demonstration flow
1. Open the home page.
2. Register a normal user and log in.
3. Submit a pickup request with item, quantity, address and date.
4. Show the request in the user dashboard as Pending.
5. Log in as the admin and change the request to Approved, Collected or Rejected.
6. Return to the user dashboard and show the updated status.
7. Visit `/health` to demonstrate the health endpoint.

## 3. DevOps demonstration
- **Git/GitHub:** show repository, branches, commit history and pull request.
- **CI:** push a commit and show the GitHub Actions run; tests and Docker image build execute automatically.
- **Docker:** run `docker compose up --build`; show web and MySQL containers with `docker compose ps`.
- **Deployment:** open the deployed URL and `/health` endpoint.

## 4. Common viva questions
**What is DevOps?** A culture and set of practices that brings development and operations together to deliver software reliably and frequently.

**Why Git?** It tracks source-code history and supports branching, collaboration and rollback.

**What is CI?** Continuous Integration automatically validates code changes, commonly through builds and tests.

**What is CD?** Continuous Delivery/Deployment automates preparing or releasing validated software.

**Why Docker?** It packages the application and its runtime dependencies into a portable container.

**Why MySQL?** It is a relational database suitable for structured users and pickup-request records.

**What does Docker Compose do?** It defines and runs multiple related containers, here Flask and MySQL.

**Why hash passwords?** A one-way password hash reduces the impact of a database leak compared with storing plaintext passwords.

**What is `/health`?** A simple endpoint used by operators or hosting platforms to check whether the web process responds.

## 5. Limitations / future scope
Add pickup-centre mapping, email/SMS notifications, QR-based collection receipts, CSV exports, request audit history, CSRF protection and automated database migrations.
