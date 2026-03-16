import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { createBook, getBook, updateBook } from "../services/bookService";
import { getAuthors } from "../services/authorService";
import "../styles/Forms.css";

export default function AddBook() {
    const { id } = useParams();
    const navigate = useNavigate();
    const isEdit = Boolean(id);

    const [form, setForm] = useState({
        title: "",
        isbn: "",
        genre: "",
        publisher: "",
        published_date: "",
        description: "",
        total_pages: "",
        total_chapters: "",
        rating: "",
        status: "unread",
        author_ids: [],
    });
    const [authors, setAuthors] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        getAuthors()
            .then((res) => setAuthors(res.data))
            .catch(() => {});

        if (isEdit) {
            getBook(id).then((res) => {
                const b = res.data;
                setForm({
                    title: b.title || "",
                    isbn: b.isbn || "",
                    genre: b.genre || "",
                    publisher: b.publisher || "",
                    published_date: b.published_date || "",
                    description: b.description || "",
                    total_pages: b.total_pages || "",
                    total_chapters: b.total_chapters || "",
                    rating: b.rating || "",
                    status: b.status || "unread",
                    author_ids: b.authors ? b.authors.map((a) => a.id) : [],
                });
            });
        }
    }, [id, isEdit]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const handleAuthorToggle = (authorId) => {
        setForm((prev) => ({
            ...prev,
            author_ids: prev.author_ids.includes(authorId)
                ? prev.author_ids.filter((id) => id !== authorId)
                : [...prev.author_ids, authorId],
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        const data = {
            ...form,
            total_pages: form.total_pages ? parseInt(form.total_pages) : 0,
            total_chapters: form.total_chapters
                ? parseInt(form.total_chapters)
                : 0,
            rating: form.rating ? parseInt(form.rating) : null,
        };

        try {
            if (isEdit) {
                await updateBook(id, data);
            } else {
                await createBook(data);
            }
            navigate("/books");
        } catch (err) {
            setError(err.response?.data?.message || "Failed to save book");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="form-page">
            <h1>{isEdit ? "Edit Book" : "Add Book"}</h1>
            {error && <p className="error">{error}</p>}

            <form onSubmit={handleSubmit} className="form">
                <div className="form-group">
                    <label htmlFor="title">Title *</label>
                    <input
                        id="title"
                        name="title"
                        type="text"
                        value={form.title}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="isbn">ISBN</label>
                        <input
                            id="isbn"
                            name="isbn"
                            type="text"
                            value={form.isbn}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="genre">Genre</label>
                        <input
                            id="genre"
                            name="genre"
                            type="text"
                            value={form.genre}
                            onChange={handleChange}
                        />
                    </div>
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="publisher">Publisher</label>
                        <input
                            id="publisher"
                            name="publisher"
                            type="text"
                            value={form.publisher}
                            onChange={handleChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="published_date">Published Date</label>
                        <input
                            id="published_date"
                            name="published_date"
                            type="text"
                            value={form.published_date}
                            onChange={handleChange}
                            placeholder="e.g. 2024"
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label htmlFor="description">Description</label>
                    <textarea
                        id="description"
                        name="description"
                        value={form.description}
                        onChange={handleChange}
                        rows={4}
                    />
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="total_pages">Total Pages</label>
                        <input
                            id="total_pages"
                            name="total_pages"
                            type="number"
                            value={form.total_pages}
                            onChange={handleChange}
                            min={0}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="total_chapters">Total Chapters</label>
                        <input
                            id="total_chapters"
                            name="total_chapters"
                            type="number"
                            value={form.total_chapters}
                            onChange={handleChange}
                            min={0}
                        />
                    </div>
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="status">Status</label>
                        <select
                            id="status"
                            name="status"
                            value={form.status}
                            onChange={handleChange}
                        >
                            <option value="unread">Unread</option>
                            <option value="reading">Reading</option>
                            <option value="completed">Completed</option>
                            <option value="on_hold">On Hold</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label htmlFor="rating">Rating</label>
                        <select
                            id="rating"
                            name="rating"
                            value={form.rating}
                            onChange={handleChange}
                        >
                            <option value="">No rating</option>
                            <option value="1">1 - Poor</option>
                            <option value="2">2 - Fair</option>
                            <option value="3">3 - Good</option>
                            <option value="4">4 - Very Good</option>
                            <option value="5">5 - Excellent</option>
                        </select>
                    </div>
                </div>

                {authors.length > 0 && (
                    <div className="form-group">
                        <label>Authors</label>
                        <div className="checkbox-group">
                            {authors.map((author) => (
                                <label
                                    key={author.id}
                                    className="checkbox-label"
                                >
                                    <input
                                        type="checkbox"
                                        checked={form.author_ids.includes(
                                            author.id,
                                        )}
                                        onChange={() =>
                                            handleAuthorToggle(author.id)
                                        }
                                    />
                                    {author.name}
                                </label>
                            ))}
                        </div>
                    </div>
                )}

                <div className="form-actions">
                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading}
                    >
                        {loading
                            ? "Saving..."
                            : isEdit
                              ? "Update Book"
                              : "Add Book"}
                    </button>
                    <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => navigate(-1)}
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
}
