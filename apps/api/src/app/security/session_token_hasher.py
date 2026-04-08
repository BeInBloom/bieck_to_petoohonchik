from hashlib import sha256


class SessionTokenHasher:
    def hash(self, raw_token: str) -> str:
        return sha256(raw_token.encode("utf-8")).hexdigest()
