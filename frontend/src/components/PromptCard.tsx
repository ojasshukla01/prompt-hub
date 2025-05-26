// src/components/PromptCard.tsx

import React from "react";

interface PromptCardProps {
  title: string;
  content: string;
  tags: string[];
  authorUsername: string;
}

const PromptCard: React.FC<PromptCardProps> = ({
  title,
  content,
  tags,
  authorUsername,
}) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow duration-200">
      <h2 className="text-lg font-semibold mb-2">{title}</h2>
      <p className="text-gray-600 text-sm mb-3">{content.slice(0, 100)}...</p>
      <div className="flex flex-wrap gap-2 mb-3">
        {tags.map((tag, idx) => (
          <span
            key={idx}
            className="text-xs bg-gray-200 rounded-full px-2 py-1 text-gray-700"
          >
            {tag}
          </span>
        ))}
      </div>
      <p className="text-sm text-gray-500">By {authorUsername}</p>
    </div>
  );
};

export default PromptCard;
