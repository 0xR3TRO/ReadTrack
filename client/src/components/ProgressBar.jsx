import "../styles/ProgressBar.css";

export default function ProgressBar({ current, total, label }) {
    const percentage = total > 0 ? Math.round((current / total) * 100) : 0;

    return (
        <div className="progress-container">
            {label && <span className="progress-label">{label}</span>}
            <div className="progress-bar">
                <div
                    className="progress-fill"
                    style={{ width: `${percentage}%` }}
                />
            </div>
            <span className="progress-text">
                {current}/{total} ({percentage}%)
            </span>
        </div>
    );
}
