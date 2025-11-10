# v17/zstd_io.py
import zstandard as zstd
import json

class ZstdIO:
    def save(self, data):
        return zstd.ZstdCompressor().compress(json.dumps(data).encode())
    def load(self, blob):
        return json.loads(zstd.ZstdDecompressor().decompress(blob).decode())
