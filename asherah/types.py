from dataclasses import dataclass
from datetime import datetime
from typing import ByteString


@dataclass
class AsherahConfig:
    kms_type: str
    metastore: str
    service_name: str
    product_id: str
    rdbms_connection_string: str = None
    dynamo_db_endpoint: str = None
    dynamo_db_region: str = None
    dynamo_db_table_name: str = None
    enable_region_suffix: bool = False
    preferred_region: str = None
    region_map: str = None
    verbose: bool = False
    session_cache: bool = False
    debug_output: bool = False


@dataclass
class KeyMeta:
    id: str
    created: datetime


@dataclass
class EnvelopeKeyRecord:
    encrypted_key: ByteString
    created: datetime
    parent_key_meta: KeyMeta


@dataclass
class DataRowRecord:
    data: ByteString
    key: EnvelopeKeyRecord
