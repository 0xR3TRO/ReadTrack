# ReadTrack — Maintenance

## Bug Reporting

Report bugs by opening an issue in the project repository with:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Browser/OS information

## Regular Updates

### Dependency Updates

**Backend:**

```bash
cd server
pip list --outdated
pip install --upgrade <package>
# Update requirements.txt accordingly
```

**Frontend:**

```bash
cd client
npm outdated
npm update
```

### Security Patches

- Monitor dependency vulnerabilities with `npm audit` (frontend) and `pip audit` (backend).
- Update packages promptly when security advisories are published.
- Rotate `SECRET_KEY` and `JWT_SECRET_KEY` periodically in production.

## Database Maintenance

- SQLite database is stored at `server/instance/readtrack.db`.
- Back up the database file regularly in production.
- For schema migrations, consider adding Flask-Migrate (Alembic) when the schema evolves.

## File Storage

- Uploaded files are stored in `server/uploads/`.
- Monitor disk usage and implement cleanup for orphaned files if needed.
- Consider moving to cloud storage (S3, GCS) for production.

## Monitoring

- Check application logs for errors.
- Monitor API response times and error rates.
- Set up health check endpoint if deploying behind a load balancer.

## Future Improvements

- Add Flask-Migrate for database schema migrations.
- Implement pagination for book/author list endpoints.
- Add full-text search with SQLite FTS.
- Add book cover image upload and display.
- Implement book recommendations based on reading history.
- Add email verification for user registration.
- Add social sharing features.
- Implement data export (CSV, JSON).
