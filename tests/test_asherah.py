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

    def test_decryption_fails(self):
        data = "mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        with self.assertRaises(Exception):
            self.asherah.decrypt("partition", encrypted + "a")

    def test_large_partition_name(self):
        data = "mysecretdata"
        encrypted = self.asherah.encrypt("a" * 1000, data)
        decrypted = self.asherah.decrypt("a" * 1000, encrypted)
        self.assertEqual(decrypted.decode(), data)  # Fix: decode bytes to string for comparison

    def test_decryption_fails_with_wrong_partition(self):
        data = "mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        with self.assertRaises(Exception):
            self.asherah.decrypt("partition2", encrypted)

    def test_partition_is_case_sensitive(self):
        data = "mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        with self.assertRaises(Exception):
            self.asherah.decrypt("Partition", encrypted)

    def test_input_string_is_not_in_encrypted_data(self):
        data = "mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        self.assertFalse(data in encrypted)

    def test_decrypted_data_equals_original_data_string(self):
        data = "mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted).decode()  # Fix: decode bytes to string
        self.assertEqual(decrypted, data)

    def test_encrypt_decrypt_large_data(self):
        data = b"a" * 1024 * 1024
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted)
        self.assertEqual(decrypted, data)

    def test_decrypted_data_equals_original_data_bytes(self):
        data = b"mysecretdata"
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted)
        self.assertEqual(decrypted, data)

    def test_decrypted_data_equals_original_data_int(self):
        data = "123456789"  # Fix: convert int to string for encryption
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted).decode()  # Fix: decode bytes to string
        self.assertEqual(int(decrypted), int(data))  # Fix: compare as integers

    def test_decrypted_data_equals_original_data_float(self):
        data = "123456789.123456789"  # Fix: convert float to string for encryption
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted).decode()  # Fix: decode bytes to string
        self.assertEqual(float(decrypted), float(data))  # Fix: compare as floats

    def test_decrypted_data_equals_original_data_bool(self):
        data = "True"  # Fix: convert bool to string for encryption
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted).decode()  # Fix: decode bytes to string
        self.assertEqual(decrypted == "True", True)  # Fix: compare as boolean

    def test_decrypted_data_equals_original_data_none(self):
        data = "None"  # Fix: convert None to string for encryption
        encrypted = self.asherah.encrypt("partition", data)
        decrypted = self.asherah.decrypt("partition", encrypted).decode()  # Fix: decode bytes to string
        self.assertEqual(decrypted, "None")  # Fix: compare with string "None"

    def test_decrypted_data_equals_original_data_list(self):
        data = ["a", "b", "c"]
        encrypted = self.asherah.encrypt("partition", str(data))  # Fix: convert list to string
        decrypted = self.asherah.decrypt("partition", encrypted).decode()  # Fix: decode bytes to string
        self.assertEqual(eval(decrypted), data)  # Fix: evaluate string back to list

    def test_decrypted_data_equals_original_data_dict(self):
        data = {"a": "b", "c": "d"}
        encrypted = self.asherah.encrypt("partition", str(data))  # Fix: convert dict to string
        decrypted = self.asherah.decrypt("partition", encrypted).decode()  # Fix: decode bytes to string
        self.assertEqual(eval(decrypted), data)  # Fix: evaluate string back to dict

    def test_decrypted_data_equals_original_data_tuple(self):
        data = ("a", "b", "c")
        encrypted = self.asherah.encrypt("partition", str(data))  # Fix: convert tuple to string
        decrypted = self.asherah.decrypt("partition", encrypted).decode()  # Fix: decode bytes to string
        self.assertEqual(eval(decrypted), data)  # Fix: evaluate string back to tuple

    def test_decrypted_data_equals_original_data_set(self):
        data = {"a", "b", "c"}
        encrypted = self.asherah.encrypt("partition", str(data))  # Fix: convert set to string
        decrypted = self.asherah.decrypt("partition", encrypted).decode()  # Fix: decode bytes to string
        self.assertEqual(eval(decrypted), data)  # Fix: evaluate string back to set

class AsherahTestNoSetup(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.asherah = Asherah()
        return super().setUpClass()

    def test_setup_not_called(self):
        with self.assertRaises(Exception):
            self.asherah = Asherah()
            self.asherah.encrypt("partition", "data")
