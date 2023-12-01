# pylint: disable=missing-function-docstring,missing-class-docstring,missing-module-docstring

from unittest import TestCase

from asherah import Asherah, AsherahConfig


class AsherahTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = AsherahConfig(
            kms="static",
            metastore="memory",
            service_name="TestService",
            product_id="TestProduct",
            verbose=True,
            enable_session_caching=True,
        )
        cls.asherah = Asherah()
        cls.asherah.setup(cls.config)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.asherah.shutdown()
        return super().tearDownClass()

    def test_input_string_is_not_in_encrypted_data(self):
        data = "mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        self.assertFalse(data in encrypted)

    def test_decrypted_data_equals_original_data_string(self):
        data = "mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted)
        self.assertEqual(decrypted, data)

    def test_encrypt_decrypt_large_data(self):
        data = b"a" * 1024 * 1024
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted)
        self.assertEqual(decrypted, data)
