"use client";

import Link from "next/link";
import { supabase } from "@/utils/supabaseClient";
import { useEffect, useState } from "react";

const Navbar = () => {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const getUser = async () => {
      const { data } = await supabase.auth.getUser();
      setUser(data.user);
    };
    getUser();
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    setUser(null);
  };

  return (
    <nav className="bg-gray-800 text-white px-4 py-2 flex justify-between items-center">
      <div className="font-bold text-lg">
        <Link href="/">PromptHub</Link>
      </div>
      <div className="space-x-4 flex items-center">
        <Link href="/explore" className="hover:text-gray-300">
          Explore
        </Link>
        <Link href="/my-prompts" className="hover:text-gray-300">
          My Prompts
        </Link>
        {user ? (
          <button onClick={handleLogout} className="hover:text-gray-300">
            Logout
          </button>
        ) : (
          <Link href="/login" className="hover:text-gray-300">
            Login
          </Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
