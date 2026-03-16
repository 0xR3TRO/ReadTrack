class TestCreateBook:
    def test_create_book(self, client, auth_headers):
        response = client.post(
            "/api/books",
            json={"title": "Test Book", "total_pages": 300},
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 201
        assert data["data"]["title"] == "Test Book"
        assert data["data"]["total_pages"] == 300
        assert data["data"]["status"] == "unread"

    def test_create_book_missing_title(self, client, auth_headers):
        response = client.post(
            "/api/books",
            json={"total_pages": 300},
            headers=auth_headers,
        )
        assert response.status_code == 400

    def test_create_book_unauthorized(self, client):
        response = client.post(
            "/api/books",
            json={"title": "Test"},
        )
        assert response.status_code == 401


class TestListBooks:
    def test_list_books_empty(self, client, auth_headers):
        response = client.get("/api/books", headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert data["data"] == []

    def test_list_books(self, client, auth_headers):
        client.post(
            "/api/books",
            json={"title": "Book 1"},
            headers=auth_headers,
        )
        client.post(
            "/api/books",
            json={"title": "Book 2"},
            headers=auth_headers,
        )
        response = client.get("/api/books", headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert len(data["data"]) == 2

    def test_list_books_filter_status(self, client, auth_headers):
        client.post(
            "/api/books",
            json={"title": "Reading Book", "status": "reading"},
            headers=auth_headers,
        )
        client.post(
            "/api/books",
            json={"title": "Unread Book"},
            headers=auth_headers,
        )
        response = client.get("/api/books?status=reading", headers=auth_headers)
        data = response.get_json()
        assert len(data["data"]) == 1
        assert data["data"][0]["title"] == "Reading Book"


class TestGetBook:
    def test_get_book(self, client, auth_headers):
        create_res = client.post(
            "/api/books",
            json={"title": "Detail Book", "genre": "Fiction"},
            headers=auth_headers,
        )
        book_id = create_res.get_json()["data"]["id"]

        response = client.get(f"/api/books/{book_id}", headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert data["data"]["title"] == "Detail Book"
        assert "notes" in data["data"]
        assert "files" in data["data"]

    def test_get_book_not_found(self, client, auth_headers):
        response = client.get("/api/books/99999", headers=auth_headers)
        assert response.status_code == 404


class TestUpdateBook:
    def test_update_book(self, client, auth_headers):
        create_res = client.post(
            "/api/books",
            json={"title": "Old Title"},
            headers=auth_headers,
        )
        book_id = create_res.get_json()["data"]["id"]

        response = client.put(
            f"/api/books/{book_id}",
            json={"title": "New Title", "genre": "Sci-Fi"},
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data["data"]["title"] == "New Title"
        assert data["data"]["genre"] == "Sci-Fi"


class TestDeleteBook:
    def test_delete_book(self, client, auth_headers):
        create_res = client.post(
            "/api/books",
            json={"title": "To Delete"},
            headers=auth_headers,
        )
        book_id = create_res.get_json()["data"]["id"]

        response = client.delete(f"/api/books/{book_id}", headers=auth_headers)
        assert response.status_code == 204

        response = client.get(f"/api/books/{book_id}", headers=auth_headers)
        assert response.status_code == 404


class TestProgress:
    def test_update_progress(self, client, auth_headers):
        create_res = client.post(
            "/api/books",
            json={"title": "Progress Book", "total_pages": 400},
            headers=auth_headers,
        )
        book_id = create_res.get_json()["data"]["id"]

        response = client.patch(
            f"/api/books/{book_id}/progress",
            json={"current_page": 150, "status": "reading"},
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data["data"]["current_page"] == 150
        assert data["data"]["status"] == "reading"
        assert data["data"]["progress_percentage"] == 37.5
