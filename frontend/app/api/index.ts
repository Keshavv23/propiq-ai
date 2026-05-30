import axios from "axios";

const API = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "https://propiq-ai-eta.vercel.app",
});

export default API;