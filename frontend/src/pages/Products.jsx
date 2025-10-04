import { useEffect, useState } from "react";
import { fetchProducts } from "../api/products";
import { Link } from "react-router-dom";

export default function Products() {
    
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetchProducts().then(setItems);
    }, []);

    return (
        <div>
            <h1>Товары</h1>
            <ul>
                {items.map(p => (
                    <li key={p.id}>
                        <Link to={`/products/${p.id}`}>{p.name}</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}