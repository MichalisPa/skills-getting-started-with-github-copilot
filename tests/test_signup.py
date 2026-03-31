import pytest


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client, sample_participant):
        """Test successful signup to an activity"""
        response = client.post(
            f"/activities/Chess%20Club/signup?email={sample_participant}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_participant in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant_to_activity(self, client, sample_participant):
        """Test that signup actually adds participant to activity list"""
        from app import activities
        
        before_count = len(activities["Chess Club"]["participants"])
        
        client.post(
            f"/activities/Chess%20Club/signup?email={sample_participant}"
        )
        
        after_count = len(activities["Chess Club"]["participants"])
        assert after_count == before_count + 1
        assert sample_participant in activities["Chess Club"]["participants"]

    def test_signup_duplicate_email_fails(self, client):
        """Test that duplicate signup returns 400 error"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_invalid_activity_fails(self, client, sample_participant):
        """Test that signup to non-existent activity returns 404"""
        response = client.post(
            f"/activities/NonExistent%20Activity/signup?email={sample_participant}"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_multiple_different_users(self, client):
        """Test that multiple users can sign up to same activity"""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        response1 = client.post(
            f"/activities/Chess%20Club/signup?email={email1}"
        )
        response2 = client.post(
            f"/activities/Chess%20Club/signup?email={email2}"
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        from app import activities
        participants = activities["Chess Club"]["participants"]
        assert email1 in participants
        assert email2 in participants

    def test_signup_email_validation(self, client):
        """Test signup with various email formats"""
        valid_email = "valid.email@mergington.edu"
        response = client.post(
            f"/activities/Programming%20Class/signup?email={valid_email}"
        )
        
        # Should accept valid email format
        assert response.status_code == 200

    def test_signup_case_sensitive_email(self, client):
        """Test that email case sensitivity is handled"""
        email_lower = "newstudent@mergington.edu"
        email_upper = "NewStudent@Mergington.edu"
        
        # First signup should succeed
        response1 = client.post(
            f"/activities/Chess%20Club/signup?email={email_lower}"
        )
        assert response1.status_code == 200
        
        # Second signup with different case should be treated as different email
        # (depending on implementation, this could be a feature or bug)
        # This test documents the current behavior
        response2 = client.post(
            f"/activities/Chess%20Club/signup?email={email_upper}"
        )
        # With current implementation, these are treated as different emails
        assert response2.status_code == 200
