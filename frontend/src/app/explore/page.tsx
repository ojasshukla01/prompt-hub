"use client";

import useSWR from "swr";
import PromptCard from "@/components/PromptCard";

type Prompt = {
  id: string;
  title: string;
  content: string;
  tags: string[];
  author: {
    username: string;
  };
};

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function ExplorePromptsPage() {
  const { data: prompts, error, isLoading } = useSWR<Prompt[]>(
    "http://127.0.0.1:8000/prompts",
    fetcher
  );

  if (isLoading) return <p className="p-4">Loading prompts...</p>;
  if (error) return <p className="p-4 text-red-500">Error loading prompts.</p>;

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Explore Prompts</h1>
      {prompts && prompts.length === 0 ? (
        <p>No prompts found.</p>
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
