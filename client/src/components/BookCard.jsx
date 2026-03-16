import { Link } from "react-router-dom";
import ProgressBar from "./ProgressBar";
import "../styles/BookCard.css";

const statusColors = {
    unread: "#6b7280",
    reading: "#3b82f6",
    completed: "#10b981",
    on_hold: "#f59e0b",
};

export default function BookCard({ book }) {
    return (
        <Link to={`/books/${book.id}`} className="book-card">
            <div className="book-card-header">
                <h3 className="book-card-title">{book.title}</h3>
                <span
                    className="book-card-status"
                    style={{
                        backgroundColor: statusColors[book.status] || "#6b7280",
                    }}
                >
                    {book.status.replace("_", " ")}
                </span>
            </div>
            {book.authors && book.authors.length > 0 && (
                <p className="book-card-authors">
                    {book.authors.map((a) => a.name).join(", ")}
                </p>
            )}
            {book.genre && <p className="book-card-genre">{book.genre}</p>}
            {book.total_pages > 0 && (
                <ProgressBar
                    current={book.current_page}
                    total={book.total_pages}
                    label="Pages"
                />
            )}
            {book.rating && (
                <div className="book-card-rating">
                    {"★".repeat(book.rating)}
                    {"☆".repeat(5 - book.rating)}
                </div>
            )}
        </Link>
    );
}
