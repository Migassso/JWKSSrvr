import unittest
import requests

class TestJKWSServer(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_jwks_endpoint(self):
        response = requests.get("http://localhost:8080/.well-known/jwks.json")
        self.assertEqual(response.status_code, 200)

    
    def test_auth_endpoint(self):
        response = requests.post("http://localhost:8080/auth")
        self.assertEqual(response.status_code, 200)  # Token successfully generated


    def test_expired_key_auth_endpoint(self):
        response = requests.post("http://localhost:8080/auth?expired=true")
        self.assertEqual(response.status_code, 400)  # No suitable key found

    
if __name__ == "__main__":
    unittest.main()
