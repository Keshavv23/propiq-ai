"use client";
import { useEffect, useState } from "react";
import API from "../../api/index";

interface Lead {
  id: string;
  name: string;
  phone: string;
  email: string;
  budget_min: number;
  budget_max: number;
  timeline: string;
  score: number;
  qualified: boolean;
  notes: string;
}

function ScoreBadge({ score }: { score: number }) {
  const color =
    score >= 80
      ? "bg-green-500/20 text-green-400 border-green-500"
      : score >= 50
      ? "bg-yellow-500/20 text-yellow-400 border-yellow-500"
      : "bg-red-500/20 text-red-400 border-red-500";
  return (
    <span className={`px-2 py-1 rounded-md border text-xs font-bold ${color}`}>
      {score}/100
    </span>
  );
}

function formatPrice(price: number) {
  if (!price) return "-";
  return `Rs.${(price / 100000).toFixed(0)}L`;
}

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    const id = localStorage.getItem("agency_id");
    if (!id) return;
    API.get(`/agencies/${id}/leads`).then((res) => {
      setLeads(res.data.leads || []);
      setLoading(false);
    });
  }, []);

  const filtered = leads.filter((l) => {
    if (filter === "qualified") return l.qualified;
    if (filter === "unqualified") return !l.qualified;
    return true;
  });

  const sorted = [...filtered].sort((a, b) => b.score - a.score);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Loading leads...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Leads</h1>
          <p className="text-gray-400 text-sm mt-1">
            {leads.length} total — {leads.filter((l) => l.qualified).length} qualified
          </p>
        </div>
        <div className="flex gap-2">
          {["all", "qualified", "unqualified"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition ${
                filter === f
                  ? "bg-blue-600 text-white"
                  : "bg-gray-800 text-gray-400 hover:text-white"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {sorted.length === 0 ? (
        <div className="bg-gray-900 rounded-xl border border-gray-800 p-12 text-center">
          <p className="text-gray-400">No leads yet.</p>
          <p className="text-gray-500 text-sm mt-2">
            Leads appear here when buyers chat with your AI agent on Telegram.
          </p>
        </div>
      ) : (
        <div className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-800 text-left">
                <th className="px-6 py-4 text-sm text-gray-400 font-medium">Buyer</th>
                <th className="px-6 py-4 text-sm text-gray-400 font-medium">Budget</th>
                <th className="px-6 py-4 text-sm text-gray-400 font-medium">Timeline</th>
                <th className="px-6 py-4 text-sm text-gray-400 font-medium">Score</th>
                <th className="px-6 py-4 text-sm text-gray-400 font-medium">Status</th>
                <th className="px-6 py-4 text-sm text-gray-400 font-medium">Notes</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map((lead, i) => (
                <tr
                  key={lead.id}
                  className={`border-b border-gray-800 hover:bg-gray-800/50 transition ${
                    i === sorted.length - 1 ? "border-0" : ""
                  }`}
                >
                  <td className="px-6 py-4">
                    <p className="font-medium text-white">{lead.name || "-"}</p>
                    <p className="text-sm text-gray-400">{lead.phone}</p>
                    {lead.email && (
                      <p className="text-sm text-gray-500">{lead.email}</p>
                    )}
                  </td>
                  <td className="px-6 py-4 text-gray-300">
                    {lead.budget_min || lead.budget_max ? (
                      <span>
                        {formatPrice(lead.budget_min)} to {formatPrice(lead.budget_max)}
                      </span>
                    ) : (
                      "-"
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-sm text-gray-300 capitalize">
                      {lead.timeline || "-"}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <ScoreBadge score={lead.score} />
                  </td>
                  <td className="px-6 py-4">
                    {lead.qualified ? (
                      <span className="px-2 py-1 bg-green-500/20 text-green-400 border border-green-500 rounded-md text-xs font-medium">
                        Qualified
                      </span>
                    ) : (
                      <span className="px-2 py-1 bg-gray-700 text-gray-400 rounded-md text-xs font-medium">
                        Unqualified
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-400 max-w-xs truncate">
                    {lead.notes || "-"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}