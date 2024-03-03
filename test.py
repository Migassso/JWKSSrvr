import unittest
import requests

class TestJKWSServer(unittest.TestCase):
    
    def setUp(self):
        # Setup code if needed
        pass
    
    def tearDown(self):
        # Teardown code if needed
        pass
    
    def test_jwks_endpoint(self):
        response = requests.get("http://localhost:8080/.well-known/jwks.json")
        self.assertEqual(response.status_code, 200)
        # Add more assertions for the response data if needed
    
    def test_auth_endpoint(self):
        response = requests.post("http://localhost:8080/auth")
        self.assertEqual(response.status_code, 200)  # Token successfully generated
        # Add more assertions for the response data if needed

    def test_expired_key_auth_endpoint(self):
        response = requests.post("http://localhost:8080/auth?expired=true")
        self.assertEqual(response.status_code, 400)  # No suitable key found
        # Add more assertions for the response data if needed

        
        # Add more test cases as needed
    
if __name__ == "__main__":
    unittest.main()
