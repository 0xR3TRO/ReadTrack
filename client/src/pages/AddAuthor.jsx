import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
    createAuthor,
    getAuthor,
    updateAuthor,
} from "../services/authorService";
import "../styles/Forms.css";

export default function AddAuthor() {
    const { id } = useParams();
    const navigate = useNavigate();
    const isEdit = Boolean(id);

    const [form, setForm] = useState({
        name: "",
        biography: "",
        birth_date: "",
        website: "",
    });
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (isEdit) {
            getAuthor(id).then((res) => {
                const a = res.data;
                setForm({
                    name: a.name || "",
                    biography: a.biography || "",
                    birth_date: a.birth_date || "",
                    website: a.website || "",
                });
            });
        }
    }, [id, isEdit]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            if (isEdit) {
                await updateAuthor(id, form);
            } else {
                await createAuthor(form);
            }
            navigate("/authors");
        } catch (err) {
            setError(err.response?.data?.message || "Failed to save author");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="form-page">
            <h1>{isEdit ? "Edit Author" : "Add Author"}</h1>
            {error && <p className="error">{error}</p>}

            <form onSubmit={handleSubmit} className="form">
                <div className="form-group">
                    <label htmlFor="name">Name *</label>
                    <input
                        id="name"
                        name="name"
                        type="text"
                        value={form.name}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="biography">Biography</label>
                    <textarea
                        id="biography"
                        name="biography"
                        value={form.biography}
                        onChange={handleChange}
                        rows={6}
                    />
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="birth_date">Birth Date</label>
                        <input
                            id="birth_date"
                            name="birth_date"
                            type="text"
                            value={form.birth_date}
                            onChange={handleChange}
                            placeholder="e.g. 1965-07-31"
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="website">Website</label>
                        <input
                            id="website"
                            name="website"
                            type="url"
                            value={form.website}
                            onChange={handleChange}
                            placeholder="https://..."
                        />
                    </div>
                </div>

                <div className="form-actions">
                    <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={loading}
                    >
                        {loading
                            ? "Saving..."
                            : isEdit
                              ? "Update Author"
                              : "Add Author"}
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
