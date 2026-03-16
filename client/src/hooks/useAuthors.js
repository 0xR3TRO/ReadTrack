import { useState, useEffect, useCallback } from "react";
import { getAuthors } from "../services/authorService";

export function useAuthors(filters = {}) {
    const [authors, setAuthors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchAuthors = useCallback(async () => {
        setLoading(true);
        try {
            const res = await getAuthors(filters);
            setAuthors(res.data);
            setError(null);
        } catch (err) {
            setError(err.response?.data?.message || "Failed to fetch authors");
        } finally {
            setLoading(false);
        }
    }, [filters.search]);

    useEffect(() => {
        fetchAuthors();
    }, [fetchAuthors]);

    return { authors, loading, error, refetch: fetchAuthors };
}
