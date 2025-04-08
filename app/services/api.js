import config from "@/postcss.config.mjs";
import axios from "axios"; //popular library used to make get put delete post htttp requests on frontend
import { headers } from "next/headers";
const API_URL = process.env.NEXT_API_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});
//requesting the interceptor for adding the auth token
//interceptor: before sending any requests it checks if the token is stored in the storage locally
// if yes then it add Authorization: brearer<token> header and let's backend authenticate it properly
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (data) => api.post("/auth/login", data),
  signup: (data) => api.post("/auth/signup", data),
  me: () => api.get("/auth/me"),
};

export const userAPI = {
  getProfile: () => api.get("/user/me"),
  updateProfile: (data) => api.put("/user/me", data),
  getAllUsers: () => api.get("/user/all"),
  getUserById: (id) => api.get(`/user/${id}`),
};

export default api;
