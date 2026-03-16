import { useState, useEffect, useCallback } from "react";
import { getBooks } from "../services/bookService";

export function useBooks(filters = {}) {
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchBooks = useCallback(async () => {
        setLoading(true);
        try {
            const res = await getBooks(filters);
            setBooks(res.data);
            setError(null);
        } catch (err) {
            setError(err.response?.data?.message || "Failed to fetch books");
        } finally {
            setLoading(false);
        }
    }, [filters.status, filters.search]);

    useEffect(() => {
        fetchBooks();
    }, [fetchBooks]);

    return { books, loading, error, refetch: fetchBooks };
}
