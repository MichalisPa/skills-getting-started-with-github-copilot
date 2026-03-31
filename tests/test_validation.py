import pytest


class TestResponseValidation:
    """Tests for response format, status codes, and error handling"""

    def test_error_response_has_detail_field(self, client, sample_participant):
        """Test that error responses include detail field"""
        response = client.post(
            f"/activities/NonExistent/signup?email={sample_participant}"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_success_response_has_message_field(self, client, sample_participant):
        """Test that success responses include message field"""
        response = client.post(
            f"/activities/Chess%20Club/signup?email={sample_participant}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_http_status_codes_are_correct(self, client):
        """Test that appropriate HTTP status codes are used"""
        # 200 OK for successful operations
        response = client.post(
            "/activities/Chess%20Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 200
        
        # 404 NOT FOUND for missing activity
        response = client.post(
            "/activities/NonExistent/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        # 400 BAD REQUEST for duplicate signup
        response = client.post(
            "/activities/Chess%20Club/signup?email=test@mergington.edu"
        )
        # Should be 400 since we already signed up this email
        assert response.status_code == 400

    def test_content_type_is_json(self, client, sample_participant):
        """Test that responses are JSON"""
        response = client.post(
            f"/activities/Chess%20Club/signup?email={sample_participant}"
        )
        
        assert response.headers["content-type"].lower().startswith("application/json")

    def test_get_activities_returns_json(self, client):
        """Test that GET /activities returns JSON"""
        response = client.get("/activities")
        
        assert response.status_code == 200
        assert response.headers["content-type"].lower().startswith("application/json")
        # Should be parseable as JSON
        data = response.json()
        assert isinstance(data, dict)

    def test_error_messages_are_descriptive(self, client):
        """Test that error messages are helpful"""
        # Test duplicate email error
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        
        assert response.status_code == 400
        data = response.json()
        detail = data["detail"].lower()
        assert "already" in detail or "duplicate" in detail or "signed up" in detail

    def test_activity_names_with_spaces_are_handled(self, client, sample_participant):
        """Test that activity names with spaces are URL encoded properly"""
        # Activity names are URL encoded with %20
        response = client.post(
            f"/activities/Programming%20Class/signup?email={sample_participant}"
        )
        
        assert response.status_code == 200

    def test_email_parameters_are_validated(self, client):
        """Test that missing email parameter is handled"""
        response = client.post(
            "/activities/Chess%20Club/signup"
        )
        
        # Should fail - email parameter is required
        assert response.status_code != 200
