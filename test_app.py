import pytest
import sys
import importlib
import json
from packaging import version
from flask import Flask
from app import app


class TestDependencyVersions:
    """Test that all dependencies are properly installed with correct versions."""

    def test_flask_version_installed(self):
        """Verify Flask is installed and version is >= 2.3.0"""
        import flask
        assert hasattr(flask, '__version__'), "Flask version attribute not found"
        assert version.parse(flask.__version__) >= version.parse("2.3.0"), \
            f"Flask version {flask.__version__} is below minimum requirement 2.3.0"

    def test_requests_version_installed(self):
        """Verify requests is installed and version is >= 2.31.0"""
        import requests
        assert hasattr(requests, '__version__'), "requests version attribute not found"
        assert version.parse(requests.__version__) >= version.parse("2.31.0"), \
            f"requests version {requests.__version__} is below minimum requirement 2.31.0"

    def test_pandas_version_installed(self):
        """Verify pandas is installed and version is >= 2.1.0"""
        import pandas
        assert hasattr(pandas, '__version__'), "pandas version attribute not found"
        assert version.parse(pandas.__version__) >= version.parse("2.1.0"), \
            f"pandas version {pandas.__version__} is below minimum requirement 2.1.0"

    def test_numpy_version_installed(self):
        """Verify numpy is installed and version is >= 1.24.0"""
        import numpy
        assert hasattr(numpy, '__version__'), "numpy version attribute not found"
        assert version.parse(numpy.__version__) >= version.parse("1.24.0"), \
            f"numpy version {numpy.__version__} is below minimum requirement 1.24.0"

    def test_all_required_modules_importable(self):
        """Verify all required modules can be imported"""
        required_modules = ['flask', 'requests', 'pandas', 'numpy']
        for module_name in required_modules:
            try:
                importlib.import_module(module_name)
            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {str(e)}")

    def test_no_deprecated_module_errors(self):
        """Verify no deprecation warnings are raised on import"""
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            import numpy as np
            import pandas as pd
            import requests
            from flask import Flask
            # Check for critical deprecation warnings
            critical_warnings = [warning for warning in w 
                                if issubclass(warning.category, DeprecationWarning)]
            assert len(critical_warnings) == 0, \
                f"Deprecation warnings found: {[str(w.message) for w in critical_warnings]}"


class TestApplicationFunctionality:
    """Test that the Flask application works correctly with new dependencies."""

    @pytest.fixture
    def client(self):
        """Create Flask test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_app_index_route_exists(self, client):
        """Test that index route is accessible"""
        response = client.get('/')
        assert response.status_code == 200, "Index route returned non-200 status"

    def test_app_returns_json(self, client):
        """Test that index route returns JSON response"""
        response = client.get('/')
        assert response.content_type == 'application/json', \
            f"Expected JSON response, got {response.content_type}"

    def test_app_returns_sum_field(self, client):
        """Test that response contains expected 'sum' field"""
        response = client.get('/')
        data = response.get_json()
        assert data is not None, "Response is not valid JSON"
        assert 'sum' in data, f"Expected 'sum' field in response, got keys: {list(data.keys())}"

    def test_app_sum_calculation_correct(self, client):
        """Test that sum calculation is correct (1+2+3=6)"""
        response = client.get('/')
        data = response.get_json()
        assert data['sum'] == 6, f"Expected sum=6, got sum={data['sum']}"

    def test_app_sum_is_integer(self, client):
        """Test that sum is returned as integer"""
        response = client.get('/')
        data = response.get_json()
        assert isinstance(data['sum'], int), \
            f"Expected sum to be int, got {type(data['sum']).__name__}"


class TestDataProcessing:
    """Test numpy and pandas functionality with upgraded versions."""

    def test_numpy_array_creation(self):
        """Test that numpy arrays can be created"""
        import numpy as np
        data = np.array([1, 2, 3])
        assert len(data) == 3, "numpy array length incorrect"
        assert data.sum() == 6, "numpy sum calculation incorrect"

    def test_pandas_dataframe_creation(self):
        """Test that pandas DataFrames can be created"""
        import pandas as pd
        import numpy as np
        data = np.array([1, 2, 3])
        df = pd.DataFrame(data, columns=["numbers"])
        assert len(df) == 3, "DataFrame length incorrect"
        assert df["numbers"].sum() == 6, "DataFrame sum calculation incorrect"

    def test_pandas_dataframe_operations(self):
        """Test advanced pandas DataFrame operations"""
        import pandas as pd
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        assert df.shape == (3, 2), "DataFrame shape incorrect"
        assert df['A'].mean() == 2.0, "DataFrame mean calculation incorrect"

    def test_numpy_advanced_operations(self):
        """Test advanced numpy operations"""
        import numpy as np
        arr = np.array([[1, 2], [3, 4]])
        assert arr.shape == (2, 2), "numpy array shape incorrect"
        assert np.sum(arr) == 10, "numpy sum calculation incorrect"


class TestRequestsLibrary:
    """Test requests library functionality."""

    def test_requests_session_creation(self):
        """Test that requests Session can be created"""
        import requests
        session = requests.Session()
        assert session is not None, "Failed to create requests Session"

    def test_requests_headers_setting(self):
        """Test that request headers can be set"""
        import requests
        session = requests.Session()
        session.headers.update({'User-Agent': 'Test-Agent/1.0'})
        assert 'User-Agent' in session.headers, "Failed to set request headers"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
