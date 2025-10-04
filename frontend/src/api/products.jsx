import axios from "axios";

const api = axios.create({
  baseURL: "/api"
});

export async function fetchProducts() {
  const res = await api.get("/products");
  return res.data;
}

export async function fetchProduct(id) {
  const res = await api.get(`/products/${id}`);
  return res.data;
}

export async function createProduct(data) {
  const res = await api.post("/admin/products", data);
  return res.data;
}

export async function updateProduct(id, data) {
  const res = await api.patch(`/admin/products/${id}`, data);
  return res.data;
}

export async function deleteProduct(id) {
  await api.delete(`/admin/products/${id}`);
}

