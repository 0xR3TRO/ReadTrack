class TestCreateNote:
    def _create_book(self, client, auth_headers):
        res = client.post(
            "/api/books",
            json={"title": "Note Book"},
            headers=auth_headers,
        )
        return res.get_json()["data"]["id"]

    def test_create_note(self, client, auth_headers):
        book_id = self._create_book(client, auth_headers)
        response = client.post(
            f"/api/books/{book_id}/notes",
            json={"content": "Great chapter!", "page_number": 42},
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 201
        assert data["data"]["content"] == "Great chapter!"
        assert data["data"]["page_number"] == 42

    def test_create_note_missing_content(self, client, auth_headers):
        book_id = self._create_book(client, auth_headers)
        response = client.post(
            f"/api/books/{book_id}/notes",
            json={"page_number": 10},
            headers=auth_headers,
        )
        assert response.status_code == 400

    def test_create_note_book_not_found(self, client, auth_headers):
        response = client.post(
            "/api/books/99999/notes",
            json={"content": "Note"},
            headers=auth_headers,
        )
        assert response.status_code == 404


class TestListNotes:
    def test_list_notes(self, client, auth_headers):
        book_res = client.post(
            "/api/books",
            json={"title": "List Notes Book"},
            headers=auth_headers,
        )
        book_id = book_res.get_json()["data"]["id"]

        client.post(
            f"/api/books/{book_id}/notes",
            json={"content": "Note 1"},
            headers=auth_headers,
        )
        client.post(
            f"/api/books/{book_id}/notes",
            json={"content": "Note 2"},
            headers=auth_headers,
        )

        response = client.get(f"/api/books/{book_id}/notes", headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert len(data["data"]) == 2


class TestUpdateNote:
    def test_update_note(self, client, auth_headers):
        book_res = client.post(
            "/api/books",
            json={"title": "Update Note Book"},
            headers=auth_headers,
        )
        book_id = book_res.get_json()["data"]["id"]

        note_res = client.post(
            f"/api/books/{book_id}/notes",
            json={"content": "Old content"},
            headers=auth_headers,
        )
        note_id = note_res.get_json()["data"]["id"]

        response = client.put(
            f"/api/books/{book_id}/notes/{note_id}",
            json={"content": "Updated content"},
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data["data"]["content"] == "Updated content"


class TestDeleteNote:
    def test_delete_note(self, client, auth_headers):
        book_res = client.post(
            "/api/books",
            json={"title": "Delete Note Book"},
            headers=auth_headers,
        )
        book_id = book_res.get_json()["data"]["id"]

        note_res = client.post(
            f"/api/books/{book_id}/notes",
            json={"content": "To delete"},
            headers=auth_headers,
        )
        note_id = note_res.get_json()["data"]["id"]

        response = client.delete(
            f"/api/books/{book_id}/notes/{note_id}",
            headers=auth_headers,
        )
        assert response.status_code == 204

        response = client.get(f"/api/books/{book_id}/notes", headers=auth_headers)
        assert len(response.get_json()["data"]) == 0
