"""Main Asherah class, for encrypting and decrypting of data"""

# pylint: disable=line-too-long

from __future__ import annotations

import json
import os
from typing import ByteString, Union
from cobhan import Cobhan
from . import exceptions, types


class Asherah:
    """The main class for providing encryption and decryption functionality"""

    ENCRYPTION_OVERHEAD = 48
    ENVELOPE_OVERHEAD = 185
    BASE64_OVERHEAD = 1.34

    def __init__(self):
        self.__cobhan = Cobhan()
        self.__libasherah = self.__cobhan.load_library(
            os.path.join(os.path.dirname(__file__), "libasherah"),
            "libasherah",
            """
            void Shutdown();
            int32_t SetupJson(void* configJson);
            int32_t Decrypt(void* partitionIdPtr, void* encryptedDataPtr, void* encryptedKeyPtr, int64_t created, void* parentKeyIdPtr, int64_t parentKeyCreated, void* outputDecryptedDataPtr);
            int32_t Encrypt(void* partitionIdPtr, void* dataPtr, void* outputEncryptedDataPtr, void* outputEncryptedKeyPtr, void* outputCreatedPtr, void* outputParentKeyIdPtr, void* outputParentKeyCreatedPtr);
            int32_t EncryptToJson(void* partitionIdPtr, void* dataPtr, void* jsonPtr);
            int32_t DecryptFromJson(void* partitionIdPtr, void* jsonPtr, void* dataPtr);
            """,
        )

    def setup(self, config: types.AsherahConfig) -> None:
        """Set up/initialize the underlying encryption library."""
        self.ik_overhead = len(config.service_name) + len(config.product_id)
        config_json = json.dumps(config.to_json())
        config_buf = self.__cobhan.str_to_buf(config_json)
        result = self.__libasherah.SetupJson(config_buf)
        if result < 0:
            raise exceptions.AsherahException(
                f"Setup failed with error number {result}"
            )

    def shutdown(self):
        """Shut down and clean up the Asherah instance"""
        self.__libasherah.Shutdown()

    def encrypt(self, partition_id: str, data: Union[ByteString, str]):
        """Encrypt a chunk of data"""
        if isinstance(data, str):
            data = data.encode("utf-8")
        # Inputs
        partition_id_buf = self.__cobhan.str_to_buf(partition_id)
        data_buf = self.__cobhan.bytearray_to_buf(data)
        # Outputs
        buffer_estimate = int(
            self.ENVELOPE_OVERHEAD
            + self.ik_overhead
            + len(partition_id_buf)
            + ((len(data_buf) + self.ENCRYPTION_OVERHEAD) * self.BASE64_OVERHEAD)
        )
        json_buf = self.__cobhan.allocate_buf(buffer_estimate)

        result = self.__libasherah.EncryptToJson(partition_id_buf, data_buf, json_buf)
        if result < 0:
            raise exceptions.AsherahException(
                f"Encrypt failed with error number {result}"
            )
        return self.__cobhan.buf_to_str(json_buf)

    def decrypt(self, partition_id: str, data_row_record: str) -> bytearray:
        """Decrypt data that was previously encrypted by Asherah"""
        # Inputs
        partition_id_buf = self.__cobhan.str_to_buf(partition_id)
        json_buf = self.__cobhan.str_to_buf(data_row_record)

        # Output
        data_buf = self.__cobhan.allocate_buf(len(json_buf))

        result = self.__libasherah.DecryptFromJson(
            partition_id_buf,
            json_buf,
            data_buf,
        )

        if result < 0:
            raise exceptions.AsherahException(
                f"Decrypt failed with error number {result}"
            )

        return self.__cobhan.buf_to_bytearray(data_buf)
