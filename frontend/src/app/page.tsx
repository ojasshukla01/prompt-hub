"use client";

import { useEffect, useState } from "react";

type Prompt = {
  id: string;
  title: string;
  content: string;
  tags: string[];
};

export default function HomePage() {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPrompts = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/prompts");
        if (!res.ok) {
          throw new Error("Failed to fetch prompts");
        }
        const data = await res.json();
        setPrompts(data);
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPrompts();
  }, []);

  if (loading) {
    return <p className="p-4">Loading prompts...</p>;
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">All Prompts</h1>
      {prompts.length === 0 ? (
        <p>No prompts found.</p>
      ) : (
        <ul className="space-y-4">
          {prompts.map((prompt) => (
            <li key={prompt.id} className="border p-4 rounded shadow">
              <h2 className="text-xl font-bold mb-2">{prompt.title}</h2>
              <p>{prompt.content}</p>
              <div className="mt-2 text-sm text-gray-600">
                Tags: {prompt.tags.join(", ")}
              </div>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
