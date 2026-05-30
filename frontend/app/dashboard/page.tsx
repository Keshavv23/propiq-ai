"use client";

import { useEffect, useState } from "react";
import API from "../api/index";

interface Stats {
  agency: string;
  total_listings: number;
  total_leads: number;
  qualified_leads: number;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const id = localStorage.getItem("agency_id");

        if (!id) {
          setLoading(false);
          return;
        }

        const [listingsRes, leadsRes] = await Promise.all([
          API.get(`/agencies/${id}/listings`),
          API.get(`/agencies/${id}/leads`),
        ]);

        setStats({
          agency: listingsRes.data.agency || "Agency",
          total_listings: listingsRes.data.total_listings || 0,
          total_leads: leadsRes.data.total_leads || 0,
          qualified_leads: leadsRes.data.qualified_leads || 0,
        });
      } catch (error) {
        console.error("Dashboard error:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400 text-lg">
          Loading...
        </div>
      </div>
    );
  }

  const cards = [
    {
      label: "Active Listings",
      value: stats?.total_listings || 0,
      color: "blue",
    },
    {
      label: "Total Leads",
      value: stats?.total_leads || 0,
      color: "purple",
    },
    {
      label: "Qualified Leads",
      value: stats?.qualified_leads || 0,
      color: "green",
    },
    {
      label: "Conversion Rate",
      value:
        stats?.total_leads && stats.total_leads > 0
          ? `${Math.round(
              (stats.qualified_leads / stats.total_leads) * 100
            )}%`
          : "0%",
      color: "amber",
    },
  ];

  const colorMap: Record<string, string> = {
    blue: "border-blue-500 bg-blue-500/10 text-blue-400",
    purple: "border-purple-500 bg-purple-500/10 text-purple-400",
    green: "border-green-500 bg-green-500/10 text-green-400",
    amber: "border-amber-500 bg-amber-500/10 text-amber-400",
  };

  return (
    <div className="p-6">
      {/* Header */}
      <h1 className="text-3xl font-bold text-white mb-2">
        Welcome back, {stats?.agency}
      </h1>

      <p className="text-gray-400 mb-8">
        Here is what is happening with your listings today.
      </p>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        {cards.map((card) => (
          <div
            key={card.label}
            className={`rounded-xl border p-6 ${colorMap[card.color]}`}
          >
            <p className="text-sm text-gray-400 mb-1">
              {card.label}
            </p>

            <p className="text-4xl font-bold text-white">
              {card.value}
            </p>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">
        <h2 className="text-lg font-semibold text-white mb-4">
          Quick Actions
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">

          <a
            href="/dashboard/leads"
            className="bg-gray-800 hover:bg-gray-700 rounded-lg p-4 transition"
          >
            <p className="font-medium text-white">
              View Leads
            </p>

            <p className="text-sm text-gray-400 mt-1">
              See all buyer enquiries
            </p>
          </a>

          <a
            href="/dashboard/listings"
            className="bg-gray-800 hover:bg-gray-700 rounded-lg p-4 transition"
          >
            <p className="font-medium text-white">
              Manage Listings
            </p>

            <p className="text-sm text-gray-400 mt-1">
              View your properties
            </p>
          </a>

          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gray-800 hover:bg-gray-700 rounded-lg p-4 transition"
          >
            <p className="font-medium text-white">
              API Docs
            </p>

            <p className="text-sm text-gray-400 mt-1">
              Test endpoints directly
            </p>
          </a>

        </div>
      </div>
    </div>
  );
}