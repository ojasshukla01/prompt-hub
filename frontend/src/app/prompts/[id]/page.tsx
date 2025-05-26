"use client";

import { useParams } from "next/navigation";
import useSWR from "swr";

type Prompt = {
  id: string;
  title: string;
  content: string;
  tags: string[];
  author: {
    username: string;
  };
  comments: { id: string; content: string; author_id: string }[];
};

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function PromptDetailsPage() {
  const { id } = useParams<{ id: string }>();

  const { data: prompt, error, isLoading } = useSWR<Prompt>(
    `http://127.0.0.1:8000/prompts/${id}`,
    fetcher
  );

  if (isLoading) return <p className="p-4">Loading prompt...</p>;
  if (error) return <p className="p-4 text-red-500">Error loading prompt.</p>;

  if (!prompt) return <p className="p-4">Prompt not found.</p>;

  return (
    <main className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-2">{prompt.title}</h1>
      <p className="text-gray-600 mb-4">By {prompt.author.username}</p>
      <p className="mb-4">{prompt.content}</p>
      <div className="flex flex-wrap gap-2 mb-4">
        {prompt.tags.map((tag) => (
          <span
            key={tag}
            className="text-xs bg-gray-200 rounded-full px-2 py-1 text-gray-700"
          >
            {tag}
          </span>
        ))}
      </div>
      <hr className="my-4" />
      <h2 className="text-lg font-semibold mb-2">Comments</h2>
      {prompt.comments && prompt.comments.length > 0 ? (
        <ul className="space-y-2">
          {prompt.comments.map((comment) => (
            <li key={comment.id} className="p-2 border rounded bg-white">
              {comment.content}
            </li>
          ))}
        </ul>
      ) : (
        <p>No comments yet.</p>
      )}
    </main>
  );
}
