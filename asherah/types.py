"""Type definitions for the Asherah library"""
# pylint: disable=too-many-instance-attributes,invalid-name

from dataclasses import dataclass
from datetime import datetime
from typing import ByteString, Optional


@dataclass
class AsherahConfig:
    """Configuration options for Asherah setup"""

    kms_type: str
    metastore: str
    service_name: str
    product_id: str
    rdbms_connection_string: Optional[str] = None
    dynamo_db_endpoint: Optional[str] = None
    dynamo_db_region: Optional[str] = None
    dynamo_db_table_name: Optional[str] = None
    enable_region_suffix: bool = False
    preferred_region: Optional[str] = None
    region_map: Optional[str] = None
    verbose: bool = False
    session_cache: bool = False
    debug_output: bool = False


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
