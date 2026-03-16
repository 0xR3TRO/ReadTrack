import { useState } from "react";
import { uploadFile, deleteFile, downloadFile } from "../services/fileService";
import "../styles/FileUpload.css";

export default function FileUpload({ bookId, files, onUpdate }) {
    const [error, setError] = useState(null);
    const [uploading, setUploading] = useState(false);

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setUploading(true);
        try {
            await uploadFile(bookId, file);
            setError(null);
            onUpdate();
        } catch (err) {
            setError(err.response?.data?.message || "Failed to upload file");
        } finally {
            setUploading(false);
            e.target.value = "";
        }
    };

    const handleDownload = async (fileId, originalFilename) => {
        try {
            const response = await downloadFile(bookId, fileId);
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", originalFilename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            setError(err.response?.data?.message || "Failed to download file");
        }
    };

    const handleDelete = async (fileId) => {
        try {
            await deleteFile(bookId, fileId);
            onUpdate();
        } catch (err) {
            setError(err.response?.data?.message || "Failed to delete file");
        }
    };

    const formatSize = (bytes) => {
        if (!bytes) return "N/A";
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
        return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    };

    return (
        <div className="file-upload">
            <h3>Files</h3>
            {error && <p className="error">{error}</p>}

            <label className="file-input-label">
                <input
                    type="file"
                    onChange={handleUpload}
                    disabled={uploading}
                />
                {uploading ? "Uploading..." : "Choose File"}
            </label>

            <div className="file-list">
                {files && files.length > 0 ? (
                    files.map((file) => (
                        <div key={file.id} className="file-item">
                            <div className="file-info">
                                <span className="file-name">
                                    {file.original_filename}
                                </span>
                                <span className="file-size">
                                    {formatSize(file.file_size)}
                                </span>
                            </div>
                            <div className="file-actions">
                                <button
                                    onClick={() =>
                                        handleDownload(
                                            file.id,
                                            file.original_filename,
                                        )
                                    }
                                    className="btn-small"
                                >
                                    Download
                                </button>
                                <button
                                    onClick={() => handleDelete(file.id)}
                                    className="btn-delete"
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className="empty">No files yet.</p>
                )}
            </div>
        </div>
    );
}
