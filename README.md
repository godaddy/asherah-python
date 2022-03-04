# asherah-python

Asherah envelope encryption and key rotation library

This is a wrapper of the Asherah Go implementation using the Cobhan FFI library

Example code:

```python
from asherah import Asherah, AsherahConfig

config = AsherahConfig(
    kms_type='static',
    metastore='memory',
    service_name='TestService',
    product_id='TestProduct',
    verbose=True,
    session_cache=True
)
crypt = Asherah()
crypt.setup(config)

data = b"mysecretdata"

encrypted = crypt.encrypt("partition", data)
print(encrypted)

decrypted = crypt.decrypt("partition", encrypted)
print(decrypted)
```
