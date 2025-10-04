
export default function ProductCard({ product }) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        padding: "1rem",
        marginBottom: "1rem",
        borderRadius: "6px",
      }}
    >
      <h3>{product.name}</h3>
      {product.mainImageUrl && (
        <img
          src={product.mainImageUrl}
          alt={product.name}
          style={{ maxWidth: "150px" }}
        />
      )}
      <p>{product.description}</p>
      <strong>{product.price} ₽</strong>
    </div>
  );
}