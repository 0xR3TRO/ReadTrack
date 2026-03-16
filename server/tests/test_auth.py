class TestRegister:
    def test_register_success(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "password123",
            },
        )
        data = response.get_json()
        assert response.status_code == 201
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert "refresh_token" in data["data"]
        assert data["data"]["user"]["username"] == "newuser"

    def test_register_duplicate_username(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "dupuser",
                "email": "dup1@example.com",
                "password": "password123",
            },
        )
        response = client.post(
            "/api/auth/register",
            json={
                "username": "dupuser",
                "email": "dup2@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400
        assert "already exists" in response.get_json()["message"]

    def test_register_invalid_email(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "username": "emailuser",
                "email": "not-an-email",
                "password": "password123",
            },
        )
        assert response.status_code == 400

    def test_register_short_password(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "username": "shortpw",
                "email": "short@example.com",
                "password": "123",
            },
        )
        assert response.status_code == 400

    def test_register_no_body(self, client):
        response = client.post("/api/auth/register")
        assert response.status_code == 400


class TestLogin:
    def test_login_success(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "loginuser",
                "email": "login@example.com",
                "password": "password123",
            },
        )
        response = client.post(
            "/api/auth/login",
            json={"username": "loginuser", "password": "password123"},
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data["success"] is True
        assert "access_token" in data["data"]

    def test_login_wrong_password(self, client):
        client.post(
            "/api/auth/register",
            json={
                "username": "wrongpw",
                "email": "wrong@example.com",
                "password": "password123",
            },
        )
        response = client.post(
            "/api/auth/login",
            json={"username": "wrongpw", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/api/auth/login",
            json={"username": "nouser", "password": "password123"},
        )
        assert response.status_code == 401


class TestRefresh:
    def test_refresh_token(self, client, refresh_headers):
        response = client.post("/api/auth/refresh", headers=refresh_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert "access_token" in data["data"]


class TestMe:
    def test_me_success(self, client, auth_headers):
        response = client.get("/api/auth/me", headers=auth_headers)
        data = response.get_json()
        assert response.status_code == 200
        assert data["data"]["username"] == "testuser"

    def test_me_unauthorized(self, client):
        response = client.get("/api/auth/me")
        assert response.status_code == 401
