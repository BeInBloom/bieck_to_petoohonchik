from app.security.password_hasher import PasswordHasher


def test_hash_returns_encoded_password() -> None:
    hasher = PasswordHasher()

    password_hash = hasher.hash("secret-password")

    assert password_hash != "secret-password"
    assert password_hash.startswith("$argon2")


def test_verify_returns_true_for_matching_password() -> None:
    hasher = PasswordHasher()
    password_hash = hasher.hash("secret-password")

    assert hasher.verify(password_hash, "secret-password") is True


def test_verify_returns_false_for_invalid_password() -> None:
    hasher = PasswordHasher()
    password_hash = hasher.hash("secret-password")

    assert hasher.verify(password_hash, "wrong-password") is False
