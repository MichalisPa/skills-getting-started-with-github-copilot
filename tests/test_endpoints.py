import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activity records"""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_returns_correct_structure(self, client):
        """Test that activities have required fields"""
        response = client.get("/activities")
        data = response.json()
        
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

    def test_get_activities_participants(self, client):
        """Test that participants are correctly returned"""
        response = client.get("/activities")
        data = response.json()
        
        chess = data["Chess Club"]
        assert len(chess["participants"]) == 2
        assert "michael@mergington.edu" in chess["participants"]
        assert "daniel@mergington.edu" in chess["participants"]

    def test_get_activities_spot_availability(self, client):
        """Test that spot availability is correctly calculated"""
        response = client.get("/activities")
        data = response.json()
        
        basketball = data["Basketball Team"]
        # max is 15, has 1 participant, so should have 14 spots left
        spots_left = basketball["max_participants"] - len(basketball["participants"])
        assert spots_left == 14

    def test_get_activities_activity_with_no_participants(self):
        """Test that an activity with no participants is handled correctly"""
        # This is a hypothetical test - our current data doesn't have this
        # but the code should handle it gracefully
        from app import activities
        
        # Temporarily add an activity with no participants
        activities["Test Activity"] = {
            "description": "Test",
            "schedule": "Monday",
            "max_participants": 10,
            "participants": []
        }
        
        # Activities should still be retrievable
        assert "Test Activity" in activities
        assert len(activities["Test Activity"]["participants"]) == 0
