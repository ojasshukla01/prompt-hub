# Project Plan: PromptHub (Enhanced PromptHackers)

## 🎯 Project Overview

**PromptHub** is a refined, community-driven platform for creating, managing, and sharing AI prompts. It addresses the key drawbacks of the existing Prompthackers website and introduces robust features for enhanced usability, functionality, and community interactions.

**Goals:**
- Deliver a seamless, intuitive user interface.
- Enable comprehensive prompt management (organization, versioning, sharing).
- Foster a vibrant, interactive community.
- Ensure accessibility and performance across devices.
- Build using only free and open-source tools.

**Target Audience:**
- AI enthusiasts and prompt engineers.
- Content creators and marketers.
- Educators and students.
- Developers and researchers.

---

## 🛠️ Technology Stack

| Component         | Technology                       | Justification                                                                 |
|-------------------|----------------------------------|-------------------------------------------------------------------------------|
| **Frontend**      | Next.js with Tailwind CSS        | Server-side rendering, SEO benefits, modern UI.                              |
| **Backend**       | FastAPI (Python)                 | High-performance, asynchronous APIs.                                          |
| **Database**      | PostgreSQL                       | Reliable, scalable relational database.                                       |
| **Authentication**| Supabase Auth with Google OAuth  | Seamless, secure login; user tracking.                                        |
| **Hosting**       | Vercel (frontend), Railway (backend) | Free tiers, easy CI/CD.                                                     |

---

## 🧱 Data Model

### User
- `id`: UUID
- `username`: string
- `email`: string
- `profile_picture`: URL
- `bio`: text
- `created_at`: timestamp
- `updated_at`: timestamp

### Prompt
- `id`: UUID
- `title`: string
- `content`: text
- `tags`: array of strings
- `visibility`: enum (public/private)
- `version_history`: JSONB (array of past versions)
- `author_id`: UUID (foreign key to User)
- `created_at`: timestamp
- `updated_at`: timestamp

### Comment
- `id`: UUID
- `prompt_id`: UUID (foreign key to Prompt)
- `author_id`: UUID (foreign key to User)
- `content`: text
- `created_at`: timestamp

### Follow
- `follower_id`: UUID (foreign key to User)
- `following_id`: UUID (foreign key to User)

---

## 🔌 API Design

| Endpoint                     | Method | Description                             |
|------------------------------|--------|-----------------------------------------|
| `/api/auth/login`            | POST   | Authenticate user via Google OAuth      |
| `/api/auth/logout`           | POST   | Logout user                             |
| `/api/prompts`               | GET    | Retrieve list of prompts                |
| `/api/prompts`               | POST   | Create a new prompt                     |
| `/api/prompts/{id}`          | GET    | Retrieve a specific prompt              |
| `/api/prompts/{id}`          | PUT    | Update a prompt                         |
| `/api/prompts/{id}`          | DELETE | Delete a prompt                         |
| `/api/prompts/{id}/comments` | GET    | Retrieve comments for a prompt          |
| `/api/prompts/{id}/comments` | POST   | Add a comment to a prompt               |
| `/api/users/{id}/follow`     | POST   | Follow a user                           |
| `/api/users/{id}/unfollow`   | POST   | Unfollow a user                         |
| `/api/users/{id}`            | GET    | Retrieve user profile                   |

---

## 🎨 Frontend Architecture

- **Pages:**
  - Home
  - Explore Prompts
  - Create Prompt
  - My Prompts
  - Profile
  - Community Discussions

- **Components:**
  - Navigation Bar
  - Prompt Card
  - Prompt Editor
  - Comment Section
  - User Profile
  - Follow Button
  - Search and Filter

- **State Management:**
  - React Context API for global state
  - SWR for data fetching and caching

---

## 🧰 Backend Architecture

- FastAPI app with modular routers for each resource.
- PostgreSQL database via SQLAlchemy.
- Authentication via Supabase Auth & JWT tokens.
- Automatic API docs (FastAPI’s Swagger).
- Error handling with custom exception handlers.

---

## 🚀 Deployment Plan

- **Frontend:**
  - Deployed on Vercel with GitHub integration.
  - Environment variables for API endpoints.

- **Backend:**
  - Deployed on Railway with PostgreSQL DB.
  - Secure environment variables for DB and Supabase keys.

- **CI/CD:**
  - GitHub Actions for automated testing and deployments.

---

## 🧪 Testing Plan

- **Frontend:**
  - Unit tests: Jest + React Testing Library
  - E2E tests: Cypress
  - Accessibility audits: Lighthouse & axe-core

- **Backend:**
  - Unit tests: Pytest
  - Integration tests: HTTPX

- **Performance:**
  - Lighthouse performance metrics for frontend.
  - Database performance monitoring.

---

## 📅 Timeline

| Phase                        | Duration  |
|------------------------------|-----------|
| Project Setup & Planning     | 1 day     |
| Frontend Development         | 5 days    |
| Backend Development          | 5 days    |
| Integration & Testing        | 3 days    |
| Deployment & Monitoring      | 2 days    |
| Buffer & Final Adjustments   | 2 days    |
| **Total Estimated**          | **18 days** |

---

## ✅ Verification

- Validate functionality of each core feature.
- Conduct comprehensive testing for UI, performance, and accessibility.
- Confirm that Supabase Auth with Google OAuth works correctly.
- Review feedback from initial users.

---

## 🔜 Next Steps

Move on to **Step 2: Setting Up the GitHub Repository and Project Structure** to begin implementation!

---

