import { useState } from "react";
import { createNote, deleteNote } from "../services/noteService";
import "../styles/NoteList.css";

export default function NoteList({ bookId, notes, onUpdate }) {
    const [content, setContent] = useState("");
    const [pageNumber, setPageNumber] = useState("");
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!content.trim()) return;

        try {
            await createNote(bookId, {
                content,
                page_number: pageNumber ? parseInt(pageNumber) : null,
            });
            setContent("");
            setPageNumber("");
            setError(null);
            onUpdate();
        } catch (err) {
            setError(err.response?.data?.message || "Failed to add note");
        }
    };

    const handleDelete = async (noteId) => {
        try {
            await deleteNote(bookId, noteId);
            onUpdate();
        } catch (err) {
            setError(err.response?.data?.message || "Failed to delete note");
        }
    };

    return (
        <div className="note-list">
            <h3>Notes</h3>
            {error && <p className="error">{error}</p>}

            <form onSubmit={handleSubmit} className="note-form">
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Add a note..."
                    rows={3}
                    required
                />
                <div className="note-form-row">
                    <input
                        type="number"
                        value={pageNumber}
                        onChange={(e) => setPageNumber(e.target.value)}
                        placeholder="Page # (optional)"
                        min={0}
                    />
                    <button type="submit" className="btn btn-primary">
                        Add Note
                    </button>
                </div>
            </form>

            <div className="notes">
                {notes && notes.length > 0 ? (
                    notes.map((note) => (
                        <div key={note.id} className="note-item">
                            <div className="note-content">{note.content}</div>
                            <div className="note-meta">
                                {note.page_number && (
                                    <span>Page {note.page_number}</span>
                                )}
                                <span>
                                    {new Date(
                                        note.created_at,
                                    ).toLocaleDateString()}
                                </span>
                                <button
                                    onClick={() => handleDelete(note.id)}
                                    className="btn-delete"
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className="empty">No notes yet.</p>
                )}
            </div>
        </div>
    );
}
