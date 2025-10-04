import { useEffect, useState } from "react";
import {
  fetchCategories,
  createCategory,
  updateCategory,
  deleteCategory,
  fetchTags,
  createTag,
  updateTag,
  deleteTag,
} from "../api/categories";

export default function AdminProducts() {
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState({});
  const [newCategory, setNewCategory] = useState("");
  const [editingCategory, setEditingCategory] = useState(null);
  const [editCategoryName, setEditCategoryName] = useState("");

  const [newTag, setNewTag] = useState({});
  const [editingTag, setEditingTag] = useState(null);
  const [editTagName, setEditTagName] = useState("");

  useEffect(() => {
    async function loadData() {
      const cats = await fetchCategories();
      setCategories(cats);

      const tagsMap = {};
      for (const cat of cats) {
        tagsMap[cat.id] = await fetchTags(cat.id).catch(() => []);
      }
      setTags(tagsMap);
    }

    loadData();
  }, []);

  async function handleAddCategory(e) {
    e.preventDefault();
    const category = await createCategory(newCategory);
    const categoryTags = await fetchTags(category.id).catch(() => []);
    setCategories(prev => [...prev, category]);
    setTags(prev => ({ ...prev, [category.id]: categoryTags }));
    setNewCategory("");
  }

  async function handleUpdateCategory(id) {
    const updated = await updateCategory(id, editCategoryName);
    setCategories(prev => prev.map(c => (c.id === id ? updated : c)));
    setEditingCategory(null);
    setEditCategoryName("");
  }

  async function handleDeleteCategory(id) {
    await deleteCategory(id);
    setCategories(prev => prev.filter(c => c.id !== id));
    setTags(prev => {
      const copy = { ...prev };
      delete copy[id];
      return copy;
    });
  }

  async function handleAddTag(e, categoryId) {
    e.preventDefault();
    const tag = await createTag(newTag[categoryId], categoryId);
    setTags(prev => ({
      ...prev,
      [categoryId]: [...(prev[categoryId] || []), tag],
    }));
    setNewTag(prev => ({ ...prev, [categoryId]: "" }));
  }

  async function handleUpdateTag(tagId, categoryId) {
    const updated = await updateTag(tagId, editTagName, categoryId);
    setTags(prev => ({
      ...prev,
      [categoryId]: prev[categoryId].map(t =>
        t.id === tagId ? updated : t
      ),
    }));
    setEditingTag(null);
    setEditTagName("");
  }

  async function handleDeleteTag(tagId, categoryId) {
    await deleteTag(tagId);
    setTags(prev => ({
      ...prev,
      [categoryId]: prev[categoryId].filter(t => t.id !== tagId),
    }));
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Админка: товары</h1>
      <h2>Категории и теги</h2>

      <ul>
        {categories.map(c => (
          <li key={c.id} style={{ marginBottom: "12px" }}>
            {editingCategory === c.id ? (
              <>
                <input
                  value={editCategoryName}
                  onChange={e => setEditCategoryName(e.target.value)}
                />
                <button onClick={() => handleUpdateCategory(c.id)}>💾</button>
                <button onClick={() => setEditingCategory(null)}>❌</button>
              </>
            ) : (
              <>
                <b>{c.name}</b>
                <button
                  onClick={() => {
                    setEditingCategory(c.id);
                    setEditCategoryName(c.name);
                  }}
                  style={{ marginLeft: "8px" }}
                >
                  ✏️
                </button>
                <button
                  onClick={() => handleDeleteCategory(c.id)}
                  style={{ marginLeft: "5px" }}
                >
                  🗑️
                </button>
              </>
            )}

            {/* Теги */}
            <ul style={{ marginTop: "6px", marginLeft: "20px" }}>
              {(tags[c.id] || []).map(t => (
                <li key={t.id} style={{ marginBottom: "4px" }}>
                  {editingTag === t.id ? (
                    <>
                      <input
                        value={editTagName}
                        onChange={e => setEditTagName(e.target.value)}
                      />
                      <button onClick={() => handleUpdateTag(t.id, c.id)}>
                        💾
                      </button>
                      <button onClick={() => setEditingTag(null)}>❌</button>
                    </>
                  ) : (
                    <>
                      {t.name}
                      <button
                        onClick={() => {
                          setEditingTag(t.id);
                          setEditTagName(t.name);
                        }}
                        style={{ marginLeft: "6px" }}
                      >
                        ✏️
                      </button>
                      <button
                        onClick={() => handleDeleteTag(t.id, c.id)}
                        style={{ marginLeft: "4px" }}
                      >
                        🗑️
                      </button>
                    </>
                  )}
                </li>
              ))}
            </ul>

            {/* Добавление тега */}
            <form
              onSubmit={e => handleAddTag(e, c.id)}
              style={{ marginTop: "5px", marginLeft: "20px" }}
            >
              <input
                value={newTag[c.id] || ""}
                onChange={e =>
                  setNewTag(prev => ({ ...prev, [c.id]: e.target.value }))
                }
                placeholder="Новый тег"
              />
              <button type="submit" style={{ marginLeft: "5px" }}>
                ➕
              </button>
            </form>
          </li>
        ))}
      </ul>

      {/* Добавление категории */}
      <form onSubmit={handleAddCategory} style={{ marginTop: "20px" }}>
        <input
          value={newCategory}
          onChange={e => setNewCategory(e.target.value)}
          placeholder="Новая категория"
        />
        <button type="submit" style={{ marginLeft: "5px" }}>
          ➕ Добавить категорию
        </button>
      </form>
    </div>
  );
}