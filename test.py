import argparse
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

def run_tests(test_cases):
    suite = unittest.TestSuite()
    for test_case in test_cases:
        suite.addTest(TestJKWSServer(test_case))
    unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
    options = {
        "1": "Run all tests",
        "2": "Run JWKS endpoint test",
        "3": "Run Auth endpoint test",
        "4": "Run Expired key Auth endpoint test"
    }

    print("Options:")
    for key, value in options.items():
        print(f"{key}. {value}")

    selected_options = input("Select options (comma-separated): ").split(",")
    selected_tests = []

    for option in selected_options:
        option = option.strip()
        if option == "1":
            selected_tests.extend(["test_jwks_endpoint", "test_auth_endpoint", "test_expired_key_auth_endpoint"])
        elif option == "2":
            selected_tests.append("test_jwks_endpoint")
        elif option == "3":
            selected_tests.append("test_auth_endpoint")
        elif option == "4":
            selected_tests.append("test_expired_key_auth_endpoint")

    if not selected_tests:
        print("No tests selected.")
    else:
        run_tests(selected_tests)

