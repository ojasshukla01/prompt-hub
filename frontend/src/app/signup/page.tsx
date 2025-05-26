"use client";

import { useState } from "react";
import { supabase } from "@/utils/supabaseClient";

export default function SignupForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState(""); // Get from input or set default
  const [error, setError] = useState("");

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const { data: { user }, error } = await supabase.auth.signUp({
      email,
      password,
    });

    if (error) {
      setError(error.message);
      return;
    }

    if (!user) {
      setError("Failed to create user");
      return;
    }

    // Get a fresh session for the access token
    const { data: { session } } = await supabase.auth.getSession();
    
    if (!session) {
      setError("Failed to get session");
      return;
    }

    // Create local DB user profile
    await fetch("http://127.0.0.1:8000/users/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: user.id,          // Supabase UID
        email: user.email,
        username: "defaultusername",  // Or prompt user
      }),
    });

    // Call your backend to create user profile
    const res = await fetch("http://127.0.0.1:8000/users/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: user.id,         // Supabase UID
        email: user.email,
        username,            // From user input or set default
      }),
    });

    if (!res.ok) {
      const { detail } = await res.json();
      setError(detail || "Error creating user profile in backend.");
      return;
    }

    // Redirect to home or login page
    window.location.href = "/";
  };

  return (
    <form onSubmit={handleSignup}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Sign Up</button>
      {error && <p className="text-red-500">{error}</p>}
    </form>
  );
}
