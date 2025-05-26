"use client";

import { useState } from "react";

export default function CreatePromptPage() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tags, setTags] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const promptData = {
      title,
      content,
      tags: tags.split(",").map((tag) => tag.trim()),
      visibility: "public",
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/prompts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(promptData),
      });

      if (!res.ok) {
        throw new Error("Failed to create prompt");
      }

      alert("Prompt created successfully!");
      // Optionally, redirect to /explore
    } catch (error) {
      console.error("Error:", error);
      alert("Error creating prompt.");
    }
  };

  return (
    <main className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Create a New Prompt</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
        <textarea
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full p-2 border rounded"
          rows={4}
          required
        />
        <input
          type="text"
          placeholder="Tags (comma-separated)"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          className="w-full p-2 border rounded"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          Create Prompt
        </button>
      </form>
    </main>
  );
}
