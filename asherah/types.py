"""Type definitions for the Asherah library"""
# pylint: disable=too-many-instance-attributes,invalid-name

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import ByteString, Dict, Optional

from enum import Enum


class KMSType(Enum):
    aws = "aws"
    static = "static"


class MetastoreType(Enum):
    rdbms = "rdbms"
    dynamodb = "dynamodb"
    memory = "memory"


class ReadConsistencyType(Enum):
    eventual = "eventual"
    global_ = "global"
    session = "session"


@dataclass
class AsherahConfig:
    """Configuration options for Asherah setup

    :param kms: Configures the master key management service (aws or static)
    :param metastore: Determines the type of metastore to use for persisting
      types
    :param service_name: The name of the service
    :param product_id: The name of the product that owns this service
    :param connection_string: The database connection string (Required if
      metastore is rdbms)
    :param dynamo_db_endpoint: An optional endpoint URL (hostname only or fully
      qualified URI) (only supported by metastore = dynamodb)
    :param dynamo_db_region: The AWS region for DynamoDB requests (defaults to
      globally configured region) (only supported by metastore = dynamodb)
    :param dynamo_db_table_name: The table name for DynamoDB (only supported by
      metastore = dynamodb)
    :param enable_region_suffix: Configure the metastore to use regional
      suffixes (only supported by metastore = dynamodb)
    :param preferred_region: The preferred AWS region (required if kms is aws)
    :param region_map: Dictionary of REGION: ARN (required if kms is aws)
    :param verbose: Enable verbose logging output
    :param enable_session_caching: Enable shared session caching
    :param expire_after: The amount of time a key is considered valid
    :param check_interval: The amount of time before cached keys are considered
      stale
    :param replica_read_consistency: Required for Aurora sessions using write
      forwarding (eventual, global, session)
    :param session_cache_max_size: Define the maximum number of sessions to
      cache (default 1000)
    :param session_cache_max_duration: The amount of time a session will remain
      cached (default 2h)
    """

    kms: KMSType
    metastore: MetastoreType
    service_name: str
    product_id: str
    connection_string: Optional[str] = None
    dynamo_db_endpoint: Optional[str] = None
    dynamo_db_region: Optional[str] = None
    dynamo_db_table_name: Optional[str] = None
    enable_region_suffix: bool = False
    preferred_region: Optional[str] = None
    region_map: Optional[Dict[str, str]] = None
    verbose: bool = False
    enable_session_caching: bool = False
    expire_after: Optional[int] = None
    check_interval: Optional[int] = None
    replica_read_consistency: Optional[ReadConsistencyType] = None
    session_cache_max_size: Optional[int] = None
    session_cache_duration: Optional[int] = None

    def to_json(self):
        def translate_key(key):
            """Translate snake_case into camelCase."""
            parts = key.split("_")
            parts = [
                part.capitalize()
                .replace("Db", "DB")
                .replace("Id", "ID")
                .replace("Kms", "KMS")
                for part in parts
            ]
            return "".join(parts)

        return {translate_key(key): val for key, val in asdict(self).items()}


@dataclass
class KeyMeta:
    """Metadata about an encryption key"""

    id: str
    created: datetime


@dataclass
class EnvelopeKeyRecord:
    """Information about an encryption envelope"""

    encrypted_key: ByteString
    created: datetime
    parent_key_meta: KeyMeta


@dataclass
class DataRowRecord:
    """Encrypted data and its related information"""

    data: ByteString
    key: EnvelopeKeyRecord
