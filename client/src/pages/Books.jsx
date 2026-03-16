import { useState } from "react";
import { Link } from "react-router-dom";
import { useBooks } from "../hooks/useBooks";
import BookCard from "../components/BookCard";
import "../styles/Books.css";

export default function Books() {
    const [status, setStatus] = useState("");
    const [search, setSearch] = useState("");
    const { books, loading } = useBooks({
        status: status || undefined,
        search: search || undefined,
    });

    return (
        <div className="books-page">
            <div className="books-header">
                <h1>My Books</h1>
                <Link to="/books/new" className="btn btn-primary">
                    Add Book
                </Link>
            </div>

            <div className="books-filters">
                <input
                    type="text"
                    placeholder="Search books..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="search-input"
                />
                <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                    className="filter-select"
                >
                    <option value="">All Status</option>
                    <option value="unread">Unread</option>
                    <option value="reading">Reading</option>
                    <option value="completed">Completed</option>
                    <option value="on_hold">On Hold</option>
                </select>
            </div>

            {loading ? (
                <div className="loading">Loading...</div>
            ) : books.length > 0 ? (
                <div className="book-grid">
                    {books.map((book) => (
                        <BookCard key={book.id} book={book} />
                    ))}
                </div>
            ) : (
                <div className="empty-state">
                    <p>No books found.</p>
                    <Link to="/books/new" className="btn btn-primary">
                        Add a Book
                    </Link>
                </div>
            )}
        </div>
    );
}
