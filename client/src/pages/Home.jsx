import { Link } from "react-router-dom";
import { useBooks } from "../hooks/useBooks";
import BookCard from "../components/BookCard";
import ProgressBar from "../components/ProgressBar";
import "../styles/Home.css";

export default function Home() {
    const { books, loading } = useBooks();

    if (loading) return <div className="loading">Loading...</div>;

    const reading = books.filter((b) => b.status === "reading");
    const completed = books.filter((b) => b.status === "completed");
    const totalPages = books.reduce((sum, b) => sum + (b.total_pages || 0), 0);
    const readPages = books.reduce((sum, b) => sum + (b.current_page || 0), 0);

    return (
        <div className="home">
            <div className="home-header">
                <h1>Dashboard</h1>
                <Link to="/books/new" className="btn btn-primary">
                    Add Book
                </Link>
            </div>

            <div className="stats-grid">
                <div className="stat-card">
                    <h3>{books.length}</h3>
                    <p>Total Books</p>
                </div>
                <div className="stat-card">
                    <h3>{reading.length}</h3>
                    <p>Currently Reading</p>
                </div>
                <div className="stat-card">
                    <h3>{completed.length}</h3>
                    <p>Completed</p>
                </div>
                <div className="stat-card overall-progress">
                    <ProgressBar
                        current={readPages}
                        total={totalPages}
                        label="Overall"
                    />
                </div>
            </div>

            {reading.length > 0 && (
                <section className="home-section">
                    <h2>Currently Reading</h2>
                    <div className="book-grid">
                        {reading.map((book) => (
                            <BookCard key={book.id} book={book} />
                        ))}
                    </div>
                </section>
            )}

            {books.length > 0 && (
                <section className="home-section">
                    <h2>Recent Books</h2>
                    <div className="book-grid">
                        {books.slice(0, 6).map((book) => (
                            <BookCard key={book.id} book={book} />
                        ))}
                    </div>
                </section>
            )}

            {books.length === 0 && (
                <div className="empty-state">
                    <h2>Welcome to ReadTrack!</h2>
                    <p>Start by adding your first book.</p>
                    <Link to="/books/new" className="btn btn-primary">
                        Add Your First Book
                    </Link>
                </div>
            )}
        </div>
    );
}
