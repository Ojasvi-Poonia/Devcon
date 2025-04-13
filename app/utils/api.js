// import { data } from "autoprefixer";

const BASE_URL = process.env.BASEURL;

export const signup = async (payload) => {
  const res = await fetch(`${BASE_URL}/auth/signup/`, {
    method: "POST",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
};
export const login = async (payload) => {
  const res = await fetch(`${BASE_URL}/auth/login/`, {
    method: "POST",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
};
export const getMyProfile = async (token) => {
  const res = await fetch(`${BASE_URL}/user/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
};
export const updateProfile = async (token, data) => {
  const res = await fetch(`${BASE_URL}/user/update`, {
    method: "PUT",
    headers: {
      "Content-type": "application/json",
      Authorization: `Bearer${token}`,
    },
    body: JSON.stringify(data),
  });
  return res.json();
};
