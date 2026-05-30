"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import API from "./api/index";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await API.get("/agencies/");
      const agencies = res.data;
      const agency = agencies.find((a: any) => a.email === email);
      if (!agency) {
        setError("No agency found with that email.");
        setLoading(false);
        return;
      }
      localStorage.setItem("agency_id", agency.id);
      localStorage.setItem("agency_name", agency.name);
      router.push("/dashboard");
    } catch {
      setError("Something went wrong. Is your backend running?");
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-white mb-2">PropIQ AI</h1>
          <p className="text-gray-400">Agency Dashboard</p>
        </div>
        <div className="bg-gray-900 rounded-2xl p-8 border border-gray-800">
          <h2 className="text-xl font-semibold text-white mb-6">Sign in</h2>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="text-sm text-gray-400 mb-1 block">
                Agency Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="sharma@properties.com"
                required
                className="w-full bg-gray-800 text-white rounded-lg px-4 py-3 border border-gray-700 focus:outline-none focus:border-blue-500"
              />
            </div>
            {error && (
              <p className="text-red-400 text-sm">{error}</p>
            )}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition disabled:opacity-50"
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
          </form>
          <div className="mt-6 p-4 bg-gray-800 rounded-lg">
            <p className="text-gray-400 text-sm mb-2">Test accounts:</p>
            <div className="space-y-1 text-sm text-gray-300 font-mono">
              <p>sharma@properties.com</p>
              <p>info@mumbairealty.com</p>
              <p>contact@punehomes.com</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}