import unittest
from auth import auth_utils


from auth import jwt_utils

class TestAuthUtils(unittest.TestCase):
    def test_hash_and_check_password(self):
        password = "test_password_123"
        hashed = auth_utils.hash_password(password)
        self.assertTrue(auth_utils.check_password(password, hashed))
        self.assertFalse(auth_utils.check_password("wrong_password", hashed))

    def test_create_and_verify_reset_token(self):
        email = "test@example.com"
        updated_at = "2025-10-07T12:00:00"
        token = jwt_utils.create_reset_token(email, updated_at)
        valid, payload = jwt_utils.verify_reset_token(token)
        self.assertTrue(valid)
        self.assertEqual(payload["email"], email)
        self.assertEqual(payload["pwd_update"], updated_at)

if __name__ == "__main__":
    unittest.main()
