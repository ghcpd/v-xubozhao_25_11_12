"""
Pytest test cases for the Flask application.
Tests both functional logic and dependency versions.
"""
import pytest
import sys
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAppFunctionality:
    """Functional tests for application logic."""
    
    def test_index_route_exists(self, client):
        """Test that the index route exists and returns 200."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_route_returns_json(self, client):
        """Test that the index route returns valid JSON."""
        response = client.get('/')
        assert response.is_json
        data = response.get_json()
        assert isinstance(data, dict)
    
    def test_index_route_returns_sum(self, client):
        """Test that the index route returns correct sum calculation."""
        response = client.get('/')
        data = response.get_json()
        assert 'sum' in data
        # Sum of [1, 2, 3] should be 6
        assert data['sum'] == 6
        assert isinstance(data['sum'], int)


class TestDependencyVersions:
    """Environment tests for dependency versions."""
    
    def test_flask_version(self):
        """Test that Flask is installed and version is >= 3.0.0."""
        from importlib.metadata import version
        flask_version = version('flask')
        major_version = int(flask_version.split('.')[0])
        assert major_version >= 3, f"Flask version {flask_version} is too old, expected >= 3.0.0"
    
    def test_requests_version(self):
        """Test that requests is installed and version is >= 2.31.0."""
        import requests
        version = requests.__version__
        version_parts = [int(x) for x in version.split('.')]
        assert version_parts[0] >= 2, f"requests version {version} is too old"
        if version_parts[0] == 2:
            assert version_parts[1] >= 31, f"requests version {version} is too old, expected >= 2.31.0"
    
    def test_pandas_version(self):
        """Test that pandas is installed and version is >= 2.2.0."""
        import pandas as pd
        version = pd.__version__
        major_version = int(version.split('.')[0])
        assert major_version >= 2, f"pandas version {version} is too old, expected >= 2.0.0"
        if major_version == 2:
            minor_version = int(version.split('.')[1])
            assert minor_version >= 2, f"pandas version {version} is too old, expected >= 2.2.0"
    
    def test_numpy_version(self):
        """Test that numpy is installed and version is >= 1.26.0."""
        import numpy as np
        version = np.__version__
        version_parts = [int(x) for x in version.split('.')]
        assert version_parts[0] >= 1, f"numpy version {version} is too old"
        if version_parts[0] == 1:
            assert version_parts[1] >= 26, f"numpy version {version} is too old, expected >= 1.26.0"
    
    def test_pytest_version(self):
        """Test that pytest is installed and version is >= 8.0.0."""
        import pytest
        version = pytest.__version__
        major_version = int(version.split('.')[0])
        assert major_version >= 8, f"pytest version {version} is too old, expected >= 8.0.0"
    
    def test_all_imports_work(self):
        """Test that all required packages can be imported."""
        from flask import Flask, jsonify
        import requests
        import pandas as pd
        import numpy as np
        import pytest
        
        # If we get here, all imports succeeded
        assert True


class TestAppIntegration:
    """Integration tests combining dependencies and app logic."""
    
    def test_app_uses_numpy_correctly(self, client):
        """Test that the app correctly uses numpy arrays."""
        response = client.get('/')
        data = response.get_json()
        # The app creates np.array([1, 2, 3]) and sums it
        assert data['sum'] == 6
    
    def test_app_uses_pandas_correctly(self, client):
        """Test that the app correctly uses pandas DataFrames."""
        response = client.get('/')
        data = response.get_json()
        # The app creates a DataFrame and sums a column
        assert isinstance(data['sum'], int)
        assert data['sum'] > 0

