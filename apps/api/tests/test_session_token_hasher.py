from app.security.session_token_hasher import SessionTokenHasher


def test_hash_returns_stable_digest() -> None:
    hasher = SessionTokenHasher()

    assert hasher.hash("raw-token") == hasher.hash("raw-token")


def test_hash_does_not_return_raw_token() -> None:
    hasher = SessionTokenHasher()

    assert hasher.hash("raw-token") != "raw-token"
