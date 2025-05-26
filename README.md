
# PromptHub 🚀

**PromptHub** is a community-driven platform for creating, sharing, and managing AI prompts. It leverages **Supabase** for authentication and **FastAPI + PostgreSQL** for a secure and scalable backend.

---

## 🟩 Tech Stack

- **Frontend**: Next.js + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Auth**: Supabase (Google/email)
- **Hosting**: Vercel (frontend), Railway/Render (backend)

---

## ⚙️ Local Setup

### 🔹 Backend
1. Create a `.env` file if needed for DB URL.
2. Create a local Postgres DB:
    ```bash
    createdb prompthub
    ```
3. Install Python dependencies:
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```
4. Start FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

### 🔹 Frontend
1. Install Node.js dependencies:
    ```bash
    cd frontend
    npm install
    ```
2. Start Next.js dev server:
    ```bash
    npm run dev
    ```

---

## 🔑 Authentication & Users

✅ **Supabase Auth** handles signups & logins.

✅ After signup, the frontend **calls `/users/`** to create a matching local DB profile.

✅ Backend verifies Supabase JWT in all protected routes.

---

## 📂 Backend Endpoints Overview

| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| GET    | /                         | Root API health check                |
| GET    | /prompts                  | List all prompts (public)            |
| POST   | /prompts                  | Create prompt (auth required)        |
| GET    | /my-prompts               | List my prompts (auth required)      |
| POST   | /users/                   | Create user profile (after signup)   |
| GET    | /users/me                 | My profile (auth required)           |
| GET    | /admin/users/             | List all users (admin only)          |
| ...    | (comments, likes, follows)| ...                                  |

---

## 🔄 Syncing Supabase Users

After signup in frontend:

```ts
const { data: { user } } = await supabase.auth.signUp({ email, password });
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
```

✅ This ensures your local DB's `users` table matches Supabase users.

To sync existing Supabase users:
```bash
python backend/sync_supabase_users.py
```

---

## 👮‍♂️ Admin-Only Access

- Admin-only endpoints require the local user's `role` to be `"admin"`.

Example SQL:
```sql
UPDATE users SET role = 'admin' WHERE email = 'you@example.com';
```

---

## 🚀 Deployment Notes

✅ Deploy frontend (Next.js) to Vercel or Netlify.

✅ Deploy backend (FastAPI) to Railway, Render, or Google Cloud Run.

✅ Use Supabase's hosted auth.

---

## 🤝 Contributing

1. Fork this repo.
2. Create your feature branch:
    ```bash
    git checkout -b feature/my-feature
    ```
3. Commit your changes.
4. Push to the branch.
5. Open a pull request.

---

## 📄 License

MIT License

---

**Built with ❤️ by Ojas Shukla and contributors.**
