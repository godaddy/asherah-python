import gc
import timeit

from asherah import Asherah, AsherahConfig

config = AsherahConfig(
    kms="static",
    metastore="memory",
    service_name="TestService",
    product_id="TestProduct",
    enable_session_caching=True,
)
crypt = Asherah()
crypt.setup(config)

data = b"mysecretdata"

crypt_cycle = """
encrypted = crypt.encrypt("partition", data)
decrypted = crypt.decrypt("partition", encrypted)
"""

print(f'Benchmarking encrypt/decrypt round trips of "{data}".')
for loop_size in [100, 1000, 10000, 100000]:
    result = timeit.timeit(
        stmt=crypt_cycle, setup="gc.enable()", number=loop_size, globals=globals()
    )
    print(f"Executed {loop_size} iterations in {result} seconds.")
