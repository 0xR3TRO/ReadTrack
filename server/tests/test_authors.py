class TestCreateAuthor:
    def test_create_author(self, client, auth_headers):
        response = client.post(
            "/api/authors",
            json={"name": "Jane Austen", "biography": "English novelist"},
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 201
        assert data["data"]["name"] == "Jane Austen"

    def test_create_author_missing_name(self, client, auth_headers):
        response = client.post(
            "/api/authors",
            json={"biography": "No name"},
            headers=auth_headers,
        )
        assert response.status_code == 400

    def test_create_author_unauthorized(self, client):
        response = client.post(
            "/api/authors",
            json={"name": "Test"},
        )
        assert response.status_code == 401


class TestListAuthors:
    def test_list_authors(self, client, auth_headers):
        client.post(
            "/api/authors",
            json={"name": "Author 1"},
            headers=auth_headers,
        )
        client.post(
            "/api/authors",
            json={"name": "Author 2"},
            headers=auth_headers,
        )
        response = client.get("/api/authors", headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert len(data["data"]) == 2


class TestGetAuthor:
    def test_get_author(self, client, auth_headers):
        create_res = client.post(
            "/api/authors",
            json={"name": "Detail Author", "biography": "A writer"},
            headers=auth_headers,
        )
        author_id = create_res.get_json()["data"]["id"]

        response = client.get(f"/api/authors/{author_id}", headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert data["data"]["name"] == "Detail Author"

    def test_get_author_not_found(self, client, auth_headers):
        response = client.get("/api/authors/99999", headers=auth_headers)
        assert response.status_code == 404


class TestUpdateAuthor:
    def test_update_author(self, client, auth_headers):
        create_res = client.post(
            "/api/authors",
            json={"name": "Old Name"},
            headers=auth_headers,
        )
        author_id = create_res.get_json()["data"]["id"]

        response = client.put(
            f"/api/authors/{author_id}",
            json={"name": "New Name", "biography": "Updated bio"},
            headers=auth_headers,
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data["data"]["name"] == "New Name"


class TestDeleteAuthor:
    def test_delete_author(self, client, auth_headers):
        create_res = client.post(
            "/api/authors",
            json={"name": "To Delete"},
            headers=auth_headers,
        )
        author_id = create_res.get_json()["data"]["id"]

        response = client.delete(f"/api/authors/{author_id}", headers=auth_headers)
        assert response.status_code == 204

        response = client.get(f"/api/authors/{author_id}", headers=auth_headers)
        assert response.status_code == 404
