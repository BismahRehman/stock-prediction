from app.service.auth import hash_password, verify_password, create_access_token, verify_access_token

# ======================= Test hash password=====================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------


def test_hash_password_returns_string():
    password = "mypassword"

    hashed = hash_password(password)

    assert isinstance(hashed, str)
    assert hashed != password



# ======================= test_verify_password=====================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------

def test_verify_password_correct():
    password = "mypassword"
    hashed = hash_password(password)

    result = verify_password(password, hashed)

    assert result is True


# -------------------------
# TEST 1: password_wrong
# -------------------------
def test_verify_password_wrong():
    password = "mypassword"
    hashed = hash_password(password)

    result = verify_password("wrongpassword", hashed)

    assert result is False


# ======================= test_create_access_token=====================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------
def test_create_access_token_returns_string():
    data = {"sub": "test@gmail.com"}

    token = create_access_token(data)

    assert isinstance(token, str)



# ======================= test_verify_access_token =====================

# -------------------------
# TEST 1: SUCCESS CASE
# -------------------------
def test_verify_access_token_valid():
    data = {"sub": "test@gmail.com"}

    token = create_access_token(data)

    payload = verify_access_token(token)

    assert payload["sub"] == "test@gmail.com"

# -------------------------
# TEST 2: access_token_invali
# -------------------------
def test_verify_access_token_invalid():
    token = "invalid.token.string"

    payload = verify_access_token(token)

    assert payload is None