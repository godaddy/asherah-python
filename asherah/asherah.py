"""Main Asherah class, for encrypting and decrypting of data"""
# pylint: disable=line-too-long, too-many-locals

import os
from datetime import datetime, timezone
from typing import ByteString, Union

from cobhan import Cobhan

from . import exceptions, types


class Asherah:
    """The main class for providing encryption and decryption functionality"""

    KEY_SIZE = 64

    def __init__(self):
        self.__cobhan = Cobhan()
        self.__libasherah = self.__cobhan.load_library(
            os.path.join(os.path.dirname(__file__), "libasherah"),
            "libasherah",
            """
            int32_t Setup(void* kmsTypePtr, void* metastorePtr, void* rdbmsConnectionStringPtr, void* dynamoDbEndpointPtr, void* dynamoDbRegionPtr, void* dynamoDbTableNamePtr, int32_t enableRegionSuffixInt, void* serviceNamePtr, void* productIdPtr, void* preferredRegionPtr, void* regionMapPtr, int32_t verboseInt, int32_t sessionCacheInt, int32_t debugOutputInt);
            int32_t Decrypt(void* partitionIdPtr, void* encryptedDataPtr, void* encryptedKeyPtr, int64_t created, void* parentKeyIdPtr, int64_t parentKeyCreated, void* outputDecryptedDataPtr);
            int32_t Encrypt(void* partitionIdPtr, void* dataPtr, void* outputEncryptedDataPtr, void* outputEncryptedKeyPtr, void* outputCreatedPtr, void* outputParentKeyIdPtr, void* outputParentKeyCreatedPtr);
            """,
        )

    def setup(self, config: types.AsherahConfig) -> None:
        """Set up/initialize the underlying encryption library."""
        kms_type_buf = self.__cobhan.str_to_buf(config.kms_type)
        metastore_buf = self.__cobhan.str_to_buf(config.metastore)
        service_name_buf = self.__cobhan.str_to_buf(config.service_name)
        product_id_buf = self.__cobhan.str_to_buf(config.product_id)
        rdbms_connection_string_buf = self.__cobhan.str_to_buf(
            config.rdbms_connection_string
        )
        dynamo_db_endpoint_buf = self.__cobhan.str_to_buf(config.dynamo_db_endpoint)
        dynamo_db_region_buf = self.__cobhan.str_to_buf(config.dynamo_db_region)
        dynamo_db_table_name_buf = self.__cobhan.str_to_buf(config.dynamo_db_table_name)
        enable_region_suffix_int = int(config.enable_region_suffix)
        preferred_region_buf = self.__cobhan.str_to_buf(config.preferred_region)
        region_map_buf = self.__cobhan.str_to_buf(config.region_map)
        verbose_int = int(config.verbose)
        session_cache_int = int(config.session_cache)
        debug_output_int = int(config.debug_output)

        result = self.__libasherah.Setup(
            kms_type_buf,
            metastore_buf,
            rdbms_connection_string_buf,
            dynamo_db_endpoint_buf,
            dynamo_db_region_buf,
            dynamo_db_table_name_buf,
            enable_region_suffix_int,
            service_name_buf,
            product_id_buf,
            preferred_region_buf,
            region_map_buf,
            verbose_int,
            session_cache_int,
            debug_output_int,
        )
        if result < 0:
            raise exceptions.AsherahException(
                f"Setup failed with error number {result}"
            )

    def encrypt(self, partition_id: str, data: Union[ByteString, str]):
        """Encrypt a chunk of data"""
        if isinstance(data, str):
            data = data.encode("utf-8")
        # Inputs
        partition_id_buf = self.__cobhan.str_to_buf(partition_id)
        data_buf = self.__cobhan.bytearray_to_buf(data)
        # Outputs
        encrypted_data_buf = self.__cobhan.allocate_buf(len(data) + self.KEY_SIZE)
        encrypted_key_buf = self.__cobhan.allocate_buf(self.KEY_SIZE)
        created_buf = self.__cobhan.int_to_buf(0)
        parent_key_id_buf = self.__cobhan.allocate_buf(self.KEY_SIZE)
        parent_key_created_buf = self.__cobhan.int_to_buf(0)

        result = self.__libasherah.Encrypt(
            partition_id_buf,
            data_buf,
            encrypted_data_buf,
            encrypted_key_buf,
            created_buf,
            parent_key_id_buf,
            parent_key_created_buf,
        )
        if result < 0:
            raise exceptions.AsherahException(
                f"Encrypt failed with error number {result}"
            )
        data_row_record = types.DataRowRecord(
            data=self.__cobhan.buf_to_bytearray(encrypted_data_buf),
            key=types.EnvelopeKeyRecord(
                encrypted_key=self.__cobhan.buf_to_bytearray(encrypted_key_buf),
                created=datetime.fromtimestamp(
                    self.__cobhan.buf_to_int(created_buf), tz=timezone.utc
                ),
                parent_key_meta=types.KeyMeta(
                    id=self.__cobhan.buf_to_str(parent_key_id_buf),
                    created=datetime.fromtimestamp(
                        self.__cobhan.buf_to_int(parent_key_created_buf),
                        tz=timezone.utc,
                    ),
                ),
            ),
        )

        return data_row_record

    def decrypt(
        self, partition_id: str, data_row_record: types.DataRowRecord
    ) -> bytearray:
        """Decrypt data that was previously encrypted by Asherah"""
        # Inputs
        partition_id_buf = self.__cobhan.str_to_buf(partition_id)
        encrypted_data_buf = self.__cobhan.bytearray_to_buf(data_row_record.data)
        encrypted_key_buf = self.__cobhan.bytearray_to_buf(
            data_row_record.key.encrypted_key
        )
        created = int(data_row_record.key.created.timestamp())
        parent_key_id_buf = self.__cobhan.str_to_buf(
            data_row_record.key.parent_key_meta.id
        )
        parent_key_created = int(
            data_row_record.key.parent_key_meta.created.timestamp()
        )
        # Output
        data_buf = self.__cobhan.allocate_buf(len(encrypted_data_buf) + self.KEY_SIZE)

        result = self.__libasherah.Decrypt(
            partition_id_buf,
            encrypted_data_buf,
            encrypted_key_buf,
            created,
            parent_key_id_buf,
            parent_key_created,
            data_buf,
        )

        if result < 0:
            raise exceptions.AsherahException(
                f"Decrypt failed with error number {result}"
            )

        return self.__cobhan.buf_to_bytearray(data_buf)
