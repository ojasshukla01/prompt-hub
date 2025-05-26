import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://nihcevicnytxaxuxnucs.supabase.co";  // Replace with your Supabase project URL
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5paGNldmljbnl0eGF4dXhudWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgxNjU4OTIsImV4cCI6MjA2Mzc0MTg5Mn0.0rOBXoahsj7oMz69UtOyNmJJVtck8lNG5sd3bdVkyQ8";                 // Replace with your Supabase anon key

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
