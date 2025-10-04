import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchProduct } from "../api/products";

export default function Product() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);

    useEffect(() => {
        fetchProduct(id).then(setProduct);
    }, [id]);

    if (!product) return <p>Загрузка...</p>;

    return (
        <div>
            <h1>{product.name}</h1>
            <p>{product.description}</p>
            <strong>{product.price} ₽</strong>
        </div>
    );
}