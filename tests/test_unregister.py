import pytest


class TestUnregister:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client):
        """Test successful unregistration from an activity"""
        response = client.post(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "michael@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes participant from activity"""
        from app import activities
        
        email = "michael@mergington.edu"
        before_count = len(activities["Chess Club"]["participants"])
        
        client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        
        after_count = len(activities["Chess Club"]["participants"])
        assert after_count == before_count - 1
        assert email not in activities["Chess Club"]["participants"]

    def test_unregister_not_registered_fails(self, client, sample_participant):
        """Test that unregistering non-registered participant returns 400"""
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={sample_participant}"
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_unregister_invalid_activity_fails(self, client):
        """Test that unregister from non-existent activity returns 404"""
        response = client.post(
            "/activities/NonExistent%20Activity/unregister?email=test@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_unregister_multiple_from_same_activity(self, client):
        """Test removing multiple participants from same activity"""
        from app import activities
        
        activity_name = "Tennis Club"
        initial_count = len(activities[activity_name]["participants"])
        
        # Unregister first participant
        response1 = client.post(
            f"/activities/Tennis%20Club/unregister?email=sophia@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Unregister second participant
        response2 = client.post(
            f"/activities/Tennis%20Club/unregister?email=lucas@mergington.edu"
        )
        assert response2.status_code == 200
        
        final_count = len(activities[activity_name]["participants"])
        assert final_count == initial_count - 2

    def test_unregister_then_signup_same_email(self, client):
        """Test that participant can re-signup after unregistering"""
        email = "michael@mergington.edu"
        activity = "Chess%20Club"
        
        # Unregister
        response1 = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert response1.status_code == 200
        
        # Sign up again
        response2 = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response2.status_code == 200
        
        from app import activities
        assert email in activities["Chess Club"]["participants"]

    def test_unregister_duplicate_attempt_fails(self, client):
        """Test that unregistering twice returns error on second attempt"""
        email = "michael@mergington.edu"
        response1 = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response1.status_code == 200
        
        # Second attempt should fail
        response2 = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response2.status_code == 400
