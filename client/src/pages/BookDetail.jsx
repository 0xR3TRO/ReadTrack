import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getBook, updateProgress, deleteBook } from "../services/bookService";
import ProgressBar from "../components/ProgressBar";
import NoteList from "../components/NoteList";
import FileUpload from "../components/FileUpload";
import "../styles/BookDetail.css";

export default function BookDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [book, setBook] = useState(null);
    const [loading, setLoading] = useState(true);
    const [currentPage, setCurrentPage] = useState("");
    const [currentChapter, setCurrentChapter] = useState("");
    const [status, setStatus] = useState("");
    const [error, setError] = useState(null);

    const fetchBook = async () => {
        try {
            const res = await getBook(id);
            setBook(res.data);
            setCurrentPage(res.data.current_page || 0);
            setCurrentChapter(res.data.current_chapter || 0);
            setStatus(res.data.status);
        } catch {
            setError("Book not found");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchBook();
    }, [id]);

    const handleProgressUpdate = async (e) => {
        e.preventDefault();
        try {
            await updateProgress(id, {
                current_page: parseInt(currentPage) || 0,
                current_chapter: parseInt(currentChapter) || 0,
                status,
            });
            fetchBook();
        } catch (err) {
            setError(
                err.response?.data?.message || "Failed to update progress",
            );
        }
    };

    const handleDelete = async () => {
        if (!window.confirm("Are you sure you want to delete this book?"))
            return;
        try {
            await deleteBook(id);
            navigate("/books");
        } catch (err) {
            setError(err.response?.data?.message || "Failed to delete book");
        }
    };

    if (loading) return <div className="loading">Loading...</div>;
    if (error && !book) return <div className="error-page">{error}</div>;
    if (!book) return null;

    return (
        <div className="book-detail">
            <div className="book-detail-header">
                <div>
                    <h1>{book.title}</h1>
                    {book.authors && book.authors.length > 0 && (
                        <p className="book-authors">
                            by{" "}
                            {book.authors.map((a, i) => (
                                <span key={a.id}>
                                    <Link to={`/authors/${a.id}`}>
                                        {a.name}
                                    </Link>
                                    {i < book.authors.length - 1 ? ", " : ""}
                                </span>
                            ))}
                        </p>
                    )}
                </div>
                <div className="book-detail-actions">
                    <Link
                        to={`/books/${id}/edit`}
                        className="btn btn-secondary"
                    >
                        Edit
                    </Link>
                    <button onClick={handleDelete} className="btn btn-danger">
                        Delete
                    </button>
                </div>
            </div>

            <div className="book-info-grid">
                {book.genre && (
                    <div className="info-item">
                        <span className="info-label">Genre</span>
                        <span>{book.genre}</span>
                    </div>
                )}
                {book.publisher && (
                    <div className="info-item">
                        <span className="info-label">Publisher</span>
                        <span>{book.publisher}</span>
                    </div>
                )}
                {book.isbn && (
                    <div className="info-item">
                        <span className="info-label">ISBN</span>
                        <span>{book.isbn}</span>
                    </div>
                )}
                {book.published_date && (
                    <div className="info-item">
                        <span className="info-label">Published</span>
                        <span>{book.published_date}</span>
                    </div>
                )}
                {book.rating && (
                    <div className="info-item">
                        <span className="info-label">Rating</span>
                        <span>
                            {"★".repeat(book.rating)}
                            {"☆".repeat(5 - book.rating)}
                        </span>
                    </div>
                )}
            </div>

            {book.description && (
                <div className="book-description">
                    <h3>Description</h3>
                    <p>{book.description}</p>
                </div>
            )}

            <div className="progress-section">
                <h3>Reading Progress</h3>
                {book.total_pages > 0 && (
                    <ProgressBar
                        current={book.current_page}
                        total={book.total_pages}
                        label="Pages"
                    />
                )}
                {book.total_chapters > 0 && (
                    <ProgressBar
                        current={book.current_chapter}
                        total={book.total_chapters}
                        label="Chapters"
                    />
                )}

                <form onSubmit={handleProgressUpdate} className="progress-form">
                    <div className="progress-inputs">
                        <div className="form-group">
                            <label>Current Page</label>
                            <input
                                type="number"
                                value={currentPage}
                                onChange={(e) => setCurrentPage(e.target.value)}
                                min={0}
                                max={book.total_pages || 99999}
                            />
                        </div>
                        <div className="form-group">
                            <label>Current Chapter</label>
                            <input
                                type="number"
                                value={currentChapter}
                                onChange={(e) =>
                                    setCurrentChapter(e.target.value)
                                }
                                min={0}
                                max={book.total_chapters || 99999}
                            />
                        </div>
                        <div className="form-group">
                            <label>Status</label>
                            <select
                                value={status}
                                onChange={(e) => setStatus(e.target.value)}
                            >
                                <option value="unread">Unread</option>
                                <option value="reading">Reading</option>
                                <option value="completed">Completed</option>
                                <option value="on_hold">On Hold</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit" className="btn btn-primary">
                        Update Progress
                    </button>
                </form>
            </div>

            {error && <p className="error">{error}</p>}

            <div className="book-detail-sections">
                <NoteList
                    bookId={book.id}
                    notes={book.notes || []}
                    onUpdate={fetchBook}
                />
                <FileUpload
                    bookId={book.id}
                    files={book.files || []}
                    onUpdate={fetchBook}
                />
            </div>
        </div>
    );
}
