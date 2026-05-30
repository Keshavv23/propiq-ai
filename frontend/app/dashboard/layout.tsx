"use client";
import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [agencyName, setAgencyName] = useState("");

  useEffect(() => {
    const id = localStorage.getItem("agency_id");
    const name = localStorage.getItem("agency_name");
    if (!id) {
      router.push("/");
      return;
    }
    setAgencyName(name || "Agency");
  }, [router]);

  function logout() {
    localStorage.clear();
    router.push("/");
  }

  const links = [
    { href: "/dashboard", label: "Overview" },
    { href: "/dashboard/leads", label: "Leads" },
    { href: "/dashboard/listings", label: "Listings" },
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Navbar */}
      <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <span className="text-xl font-bold text-blue-400">PropIQ AI</span>
          <div className="flex gap-1">
            {links.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  pathname === l.href
                    ? "bg-blue-600 text-white"
                    : "text-gray-400 hover:text-white hover:bg-gray-800"
                }`}
              >
                {l.label}
              </Link>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-gray-400 text-sm">{agencyName}</span>
          <button
            onClick={logout}
            className="text-sm text-gray-400 hover:text-white transition"
          >
            Logout
          </button>
        </div>
      </nav>
      <main className="p-6">{children}</main>
    </div>
  );
}