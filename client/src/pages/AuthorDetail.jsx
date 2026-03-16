import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getAuthor, deleteAuthor } from "../services/authorService";
import BookCard from "../components/BookCard";
import "../styles/AuthorDetail.css";

export default function AuthorDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [author, setAuthor] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        getAuthor(id)
            .then((res) => setAuthor(res.data))
            .catch(() => setError("Author not found"))
            .finally(() => setLoading(false));
    }, [id]);

    const handleDelete = async () => {
        if (!window.confirm("Are you sure you want to delete this author?"))
            return;
        try {
            await deleteAuthor(id);
            navigate("/authors");
        } catch (err) {
            setError(err.response?.data?.message || "Failed to delete author");
        }
    };

    if (loading) return <div className="loading">Loading...</div>;
    if (error && !author) return <div className="error-page">{error}</div>;
    if (!author) return null;

    return (
        <div className="author-detail">
            <div className="author-detail-header">
                <div>
                    <h1>{author.name}</h1>
                    {author.birth_date && (
                        <p className="author-birth">
                            Born: {author.birth_date}
                        </p>
                    )}
                </div>
                <div className="author-detail-actions">
                    <Link
                        to={`/authors/${id}/edit`}
                        className="btn btn-secondary"
                    >
                        Edit
                    </Link>
                    <button onClick={handleDelete} className="btn btn-danger">
                        Delete
                    </button>
                </div>
            </div>

            {author.biography && (
                <div className="author-biography">
                    <h3>Biography</h3>
                    <p>{author.biography}</p>
                </div>
            )}

            {author.website && (
                <div className="author-website">
                    <h3>Website</h3>
                    <a
                        href={author.website}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        {author.website}
                    </a>
                </div>
            )}

            {author.books && author.books.length > 0 && (
                <div className="author-books">
                    <h3>Books</h3>
                    <div className="book-grid">
                        {author.books.map((book) => (
                            <BookCard key={book.id} book={book} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
