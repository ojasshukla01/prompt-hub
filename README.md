=======================================================================
🟩 PromptHub Project Overview
=======================================================================

PromptHub is a community-driven platform for creating, sharing, and managing AI prompts. 
It uses Supabase for authentication and FastAPI + PostgreSQL for secure backend API.

=======================================================================
🟩 Tech Stack
=======================================================================

- Frontend: Next.js + Tailwind CSS
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Auth: Supabase (Google/email)
- Hosting: Vercel (frontend), Railway/Render (backend)

=======================================================================
🟩 Local Setup Instructions
=======================================================================

🔹 Backend:
---------------------------------
1. Create a `.env` file if needed for DB URL.
2. Create a local Postgres DB:
    createdb prompthub
3. Install Python dependencies:
    cd backend
    python -m venv venv
    source venv/bin/activate  (or venv\Scripts\activate on Windows)
    pip install -r requirements.txt
4. Start FastAPI server:
    uvicorn main:app --reload

🔹 Frontend:
---------------------------------
1. Install Node.js dependencies:
    cd frontend
    npm install
2. Start Next.js dev server:
    npm run dev

=======================================================================
🟩 Authentication & Users
=======================================================================

✅ Supabase Auth handles signups & logins.

✅ After signup, the frontend calls /users/ to create a matching local DB profile.

✅ The backend verifies Supabase JWT in protected routes.

=======================================================================
🟩 Backend Endpoints Overview
=======================================================================

| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| GET    | /                         | Root API health check                |
| GET    | /prompts                  | List all prompts (public)            |
| POST   | /prompts                  | Create prompt (auth required)        |
| GET    | /my-prompts               | List my prompts (auth required)      |
| POST   | /users/                   | Create user profile (after signup)   |
| GET    | /users/me                 | My profile (auth required)           |
| GET    | /admin/users/             | List all users (admin only)          |
| ...    | (other routes for comments, likes, follows)                      |

=======================================================================
🟩 Frontend Signup Flow (Trigger User Sync)
=======================================================================

After successful Supabase signup, the frontend calls:

const { data: { user } } = await supabase.auth.signUp({
  email,
  password,
});

if (user) {
  const { data: { session } } = await supabase.auth.getSession();
  await fetch("http://127.0.0.1:8000/users/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${session.access_token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: user.id,
      email: user.email,
      username: "defaultusername",
    }),
  });
}

=======================================================================
🟩 One-Time Script: Sync Existing Supabase Users
=======================================================================

File: backend/sync_supabase_users.py

Run this script to pull existing Supabase users and create local DB profiles:
    python backend/sync_supabase_users.py

=======================================================================
🟩 Admin-Only Access
=======================================================================

Admin-only endpoints require:
- The user's role in your local users table to be "admin".

Example SQL:
    UPDATE users SET role = 'admin' WHERE email = 'you@example.com';

=======================================================================
🟩 Deployment Notes
=======================================================================

✅ Deploy frontend (Next.js) to Vercel or Netlify.
✅ Deploy backend (FastAPI) to Railway, Render, or Google Cloud Run.
✅ Use Supabase's hosted auth (no changes needed).

=======================================================================
🟩 Contributing
=======================================================================

1. Fork this repo.
2. Create your feature branch:
    git checkout -b feature/my-feature
3. Commit your changes.
4. Push to the branch.
5. Open a pull request.

=======================================================================
🟩 License
=======================================================================

MIT License

Built with ❤️ by Ojas Shukla and contributors.
=======================================================================
