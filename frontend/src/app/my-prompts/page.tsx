"use client";

import useSWR from "swr";
import PromptCard from "@/components/PromptCard";
import { supabase } from "@/utils/supabaseClient";

type Prompt = {
  id: string;
  title: string;
  content: string;
  tags: string[];
  author: { username: string };
};

const fetcher = async (url: string) => {
  const { data: { session } } = await supabase.auth.getSession();
  const accessToken = session?.access_token;

  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (!res.ok) throw new Error("Failed to fetch");

  return res.json();
};

export default function MyPromptsPage() {
  const { data: prompts, error, isLoading } = useSWR<Prompt[]>(
    "http://127.0.0.1:8000/my-prompts",
    fetcher
  );

  if (isLoading) return <p className="p-4">Loading your prompts...</p>;
  if (error) return <p className="p-4 text-red-500">Error loading prompts.</p>;

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">My Prompts</h1>
      {prompts && prompts.length === 0 ? (
        <p>You haven’t created any prompts yet.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {prompts?.map((prompt) => (
            <PromptCard
              key={prompt.id}
              title={prompt.title}
              content={prompt.content}
              tags={prompt.tags}
              authorUsername={prompt.author.username}
            />
          ))}
        </div>
      )}
    </main>
  );
}
