# Project Report Outline

1. Title: EcoCycle — E-waste Pickup and Tracking System
2. Abstract: EcoCycle is a web application that streamlines e-waste pickup requests and status tracking using a user portal and an administrator portal.
3. Problem definition: Users need a simple way to request collection; operators need a central place to manage requests.
4. Objectives: online booking, status tracking, administrative workflow, relational data storage and DevOps automation.
5. Technology: Python, Flask, HTML, CSS, MySQL, Git, GitHub Actions, Docker and Render/AWS.
6. Modules: authentication, pickup booking, user dashboard, admin dashboard and deployment pipeline.
7. Architecture: Browser → Flask application → SQLAlchemy → MySQL; GitHub Actions validates commits; Docker packages the app.
8. Database entities: User(id, name, email, password_hash, role); PickupRequest(id, user_id, item_type, quantity, address, preferred_date, notes, status, created_at).
9. Testing: home route, health endpoint, registration and login.
10. DevOps process: commit → GitHub push/PR → automated tests → Docker image build → deployment.
11. Results: demonstrate a complete pickup request lifecycle and successful CI/container execution.
12. Future enhancements: maps, collection-centre scheduling, notifications, analytics and audit trail.
