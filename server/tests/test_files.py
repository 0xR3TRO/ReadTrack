import io


class TestUploadFile:
    def _create_book(self, client, auth_headers):
        res = client.post(
            "/api/books",
            json={"title": "File Book"},
            headers=auth_headers,
        )
        return res.get_json()["data"]["id"]

    def test_upload_file(self, client, auth_headers):
        book_id = self._create_book(client, auth_headers)
        data = {
            "file": (io.BytesIO(b"test content"), "test.txt"),
        }
        response = client.post(
            f"/api/books/{book_id}/files",
            data=data,
            content_type="multipart/form-data",
            headers=auth_headers,
        )
        resp_data = response.get_json()
        assert response.status_code == 201
        assert resp_data["data"]["original_filename"] == "test.txt"
        assert resp_data["data"]["file_type"] == "txt"

    def test_upload_invalid_extension(self, client, auth_headers):
        book_id = self._create_book(client, auth_headers)
        data = {
            "file": (io.BytesIO(b"binary"), "malware.exe"),
        }
        response = client.post(
            f"/api/books/{book_id}/files",
            data=data,
            content_type="multipart/form-data",
            headers=auth_headers,
        )
        assert response.status_code == 400

    def test_upload_no_file(self, client, auth_headers):
        book_id = self._create_book(client, auth_headers)
        response = client.post(
            f"/api/books/{book_id}/files",
            headers=auth_headers,
        )
        assert response.status_code == 400

    def test_upload_book_not_found(self, client, auth_headers):
        data = {
            "file": (io.BytesIO(b"test"), "test.txt"),
        }
        response = client.post(
            "/api/books/99999/files",
            data=data,
            content_type="multipart/form-data",
            headers=auth_headers,
        )
        assert response.status_code == 404


class TestListFiles:
    def test_list_files(self, client, auth_headers):
        book_res = client.post(
            "/api/books",
            json={"title": "List Files Book"},
            headers=auth_headers,
        )
        book_id = book_res.get_json()["data"]["id"]

        client.post(
            f"/api/books/{book_id}/files",
            data={"file": (io.BytesIO(b"a"), "a.txt")},
            content_type="multipart/form-data",
            headers=auth_headers,
        )
        client.post(
            f"/api/books/{book_id}/files",
            data={"file": (io.BytesIO(b"b"), "b.pdf")},
            content_type="multipart/form-data",
            headers=auth_headers,
        )

        response = client.get(f"/api/books/{book_id}/files", headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert len(data["data"]) == 2


class TestDownloadFile:
    def test_download_file(self, client, auth_headers):
        book_res = client.post(
            "/api/books",
            json={"title": "Download Book"},
            headers=auth_headers,
        )
        book_id = book_res.get_json()["data"]["id"]

        upload_res = client.post(
            f"/api/books/{book_id}/files",
            data={"file": (io.BytesIO(b"download me"), "readme.txt")},
            content_type="multipart/form-data",
            headers=auth_headers,
        )
        file_id = upload_res.get_json()["data"]["id"]

        response = client.get(
            f"/api/books/{book_id}/files/{file_id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.data == b"download me"


class TestDeleteFile:
    def test_delete_file(self, client, auth_headers):
        book_res = client.post(
            "/api/books",
            json={"title": "Delete File Book"},
            headers=auth_headers,
        )
        book_id = book_res.get_json()["data"]["id"]

        upload_res = client.post(
            f"/api/books/{book_id}/files",
            data={"file": (io.BytesIO(b"delete me"), "del.txt")},
            content_type="multipart/form-data",
            headers=auth_headers,
        )
        file_id = upload_res.get_json()["data"]["id"]

        response = client.delete(
            f"/api/books/{book_id}/files/{file_id}",
            headers=auth_headers,
        )
        assert response.status_code == 204

        response = client.get(f"/api/books/{book_id}/files", headers=auth_headers)
        assert len(response.get_json()["data"]) == 0
