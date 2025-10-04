const CATEGORY_API = "/api/admin/products/categories";
const TAG_API = "/api/admin/products/tags";

export async function fetchCategories() {
  const res = await fetch(CATEGORY_API);
  if (!res.ok) throw new Error("Ошибка загрузки категорий");
  return res.json();
}

export async function createCategory(name) {
  const res = await fetch(CATEGORY_API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error("Ошибка создания категории");
  return res.json();
}

export async function updateCategory(id, name) {
  const res = await fetch(`${CATEGORY_API}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error("Ошибка обновления категории");
  return res.json();
}

export async function deleteCategory(id) {
  const res = await fetch(`${CATEGORY_API}/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Ошибка удаления категории");
  return res.json();
}


export async function fetchTags(categoryId) {
  const res = await fetch(`${CATEGORY_API}/${categoryId}/tags`);
  if (!res.ok) throw new Error("Ошибка загрузки тегов");
  return res.json();
}

export async function createTag(name, categoryId) {
  const res = await fetch(TAG_API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, category_id: categoryId }),
  });
  if (!res.ok) throw new Error("Ошибка создания тега");
  return res.json();
}

export async function updateTag(id, name, categoryId) {
  const res = await fetch(`${TAG_API}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, category_id: categoryId }),
  });
  if (!res.ok) throw new Error("Ошибка обновления тега");
  return res.json();
}

export async function deleteTag(id) {
  const res = await fetch(`${TAG_API}/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Ошибка удаления тега");
  return res.json();
}