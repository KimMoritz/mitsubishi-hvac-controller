import unittest
from unittest.mock import patch, Mock
from mitsubishi_hvac_controller.forms import RegistrationForm
from wtforms.validators import ValidationError


class MyTestCase(unittest.TestCase):
    def test_validate_username_not_too_long(self):
        with self.assertRaises(ValidationError):
            RegistrationForm.validate_username_not_too_long(Mock(), "this_username_is_too_long")

    def test_validate_username_not_too_short(self):
        with self.assertRaises(ValidationError):
            RegistrationForm.validate_username_not_too_short(Mock(), "sh")


if __name__ == '__main__':
    unittest.main()
