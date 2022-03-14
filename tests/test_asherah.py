# pylint: disable=missing-function-docstring,missing-class-docstring,missing-module-docstring

from unittest import TestCase

from asherah import Asherah, AsherahConfig


class AsherahTest(TestCase):
    def setUp(self) -> None:
        self.config = AsherahConfig(
            kms="static",
            metastore="memory",
            service_name="TestService",
            product_id="TestProduct",
            verbose=True,
            enable_session_caching=True,
        )
        self.asherah = Asherah()
        self.asherah.setup(self.config)
        return super().setUp()

    def tearDown(self) -> None:
        self.asherah.shutdown()
        return super().tearDown()

    def test_input_string_is_not_in_encrypted_data(self):
        data = "mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        self.assertFalse(data in encrypted)

    def test_decrypted_data_equals_original_data(self):
        data = b"mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted)
        self.assertEqual(decrypted, data)
