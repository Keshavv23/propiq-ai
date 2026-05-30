"use client";
import { useEffect, useState } from "react";
import API from "../../api/index";

interface Listing {
  id: string;
  title: string;
  city: string;
  locality: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  area_sqft: number;
  property_type: string;
  is_active: boolean;
}

export default function ListingsPage() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const id = localStorage.getItem("agency_id");
    if (!id) return;
    API.get(`/agencies/${id}/listings`).then((res) => {
      setListings(res.data.listings || []);
      setLoading(false);
    });
  }, []);

  const filtered = listings.filter(
    (l) =>
      l.title.toLowerCase().includes(search.toLowerCase()) ||
      l.locality.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Loading listings...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Listings</h1>
          <p className="text-gray-400 text-sm mt-1">
            {listings.length} active properties
          </p>
        </div>
        <input
          type="text"
          placeholder="Search listings..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-gray-800 text-white rounded-lg px-4 py-2 border border-gray-700 focus:outline-none focus:border-blue-500 text-sm w-64"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((listing) => (
          <div
            key={listing.id}
            className="bg-gray-900 rounded-xl border border-gray-800 p-5 hover:border-gray-700 transition"
          >
            <div className="flex items-start justify-between mb-3">
              <span className="text-xs font-medium px-2 py-1 bg-blue-500/20 text-blue-400 rounded-md capitalize">
                {listing.property_type}
              </span>
              <span className="text-lg font-bold text-white">
                ₹{(listing.price / 100000).toFixed(0)}L
              </span>
            </div>
            <h3 className="font-semibold text-white mb-1">{listing.title}</h3>
            <p className="text-sm text-gray-400 mb-3">
              📍 {listing.locality}, {listing.city}
            </p>
            <div className="flex gap-4 text-sm text-gray-400">
              {listing.bedrooms > 0 && (
                <span>🛏 {listing.bedrooms} BHK</span>
              )}
              <span>📐 {listing.area_sqft} sqft</span>
              {listing.bathrooms > 0 && (
                <span>🚿 {listing.bathrooms} bath</span>
              )}
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          No listings found.
        </div>
      )}
    </div>
  );
}