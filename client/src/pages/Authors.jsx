import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuthors } from "../hooks/useAuthors";
import "../styles/Authors.css";

export default function Authors() {
    const [search, setSearch] = useState("");
    const { authors, loading } = useAuthors({ search: search || undefined });

    return (
        <div className="authors-page">
            <div className="authors-header">
                <h1>Authors</h1>
                <Link to="/authors/new" className="btn btn-primary">
                    Add Author
                </Link>
            </div>

            <div className="authors-filters">
                <input
                    type="text"
                    placeholder="Search authors..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="search-input"
                />
            </div>

            {loading ? (
                <div className="loading">Loading...</div>
            ) : authors.length > 0 ? (
                <div className="author-grid">
                    {authors.map((author) => (
                        <Link
                            key={author.id}
                            to={`/authors/${author.id}`}
                            className="author-card"
                        >
                            <h3>{author.name}</h3>
                            {author.biography && (
                                <p className="author-bio">
                                    {author.biography.length > 120
                                        ? author.biography.substring(0, 120) +
                                          "..."
                                        : author.biography}
                                </p>
                            )}
                        </Link>
                    ))}
                </div>
            ) : (
                <div className="empty-state">
                    <p>No authors found.</p>
                    <Link to="/authors/new" className="btn btn-primary">
                        Add an Author
                    </Link>
                </div>
            )}
        </div>
    );
}
