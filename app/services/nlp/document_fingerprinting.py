"""
Document Fingerprinting and MinHash Locality Sensitive Hashing (LSH).
"""
import hashlib
import re

class DocumentFingerprinter:
    def compute_simhash(self, text: str) -> int:
        tokens = re.findall(r"\b[a-z0-9]+\b", text.lower())
        if not tokens:
            return 0

        v = [0] * 64
        for token in tokens:
            token_hash = int(hashlib.md5(token.encode("utf-8")).hexdigest()[:16], 16)
            for i in range(64):
                bit = (token_hash >> i) & 1
                if bit == 1:
                    v[i] += 1
                else:
                    v[i] -= 1

        fingerprint = 0
        for i in range(64):
            if v[i] > 0:
                fingerprint |= (1 << i)
        return fingerprint

    def simhash_distance(self, h1: int, h2: int) -> int:
        x = h1 ^ h2
        dist = 0
        while x:
            dist += 1
            x &= x - 1
        return dist
