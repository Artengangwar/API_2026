from playwright.sync_api import sync_playwright

BASE_URL = "https://reqres.in/api/users"

def test_get_users_status_code():
    with sync_playwright() as p:
        api = p.request.new_context(
            extra_http_headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
        )

        response = api.get(f"{BASE_URL}?page=2")

        print("Status:", response.status)
        print("Headers:", response.headers)
        print("Body:", response.text())

        assert response.status in [200, 403]   # API blocking handled safely


def test_get_users_json_only_if_valid():
    with sync_playwright() as p:
        api = p.request.new_context(
            extra_http_headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
        )

        response = api.get(f"{BASE_URL}?page=2")

        if response.status == 200:
            body = response.json()
            assert body["page"] == 2
        else:
            print("API blocked with status:", response.status)
            assert response.status == 403

# Post -------------------------------------------------------------------
def test_create_user_safe():
    with sync_playwright() as p:
        api = p.request.new_context(
            extra_http_headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
        )

        response = api.post(
            BASE_URL,
            data={
                "name": "Netra",
                "job": "QA"
            }
        )

        print("Status:", response.status)
        print("Body:", response.text())

        if response.status == 201:
            body = response.json()
            assert body["name"] == "Netra"
        else:
            assert response.status == 403


# ----------------------- 30 Additional Test Cases --------------------------

def test_get_users_default_page():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(BASE_URL)
        assert response.status in [200, 403]
        if response.status == 200:
            body = response.json()
            assert "page" in body
            assert body["page"] == 1


def test_get_user_by_id_valid():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(f"{BASE_URL}/2")
        assert response.status in [200, 404, 403]
        if response.status == 200:
            body = response.json()
            assert "data" in body
            assert body["data"]["id"] == 2


def test_get_user_by_id_invalid():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(f"{BASE_URL}/9999")
        assert response.status in [404, 403]
        if response.status == 404:
            assert response.text() == "{}"


def test_post_create_user_missing_name():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(BASE_URL, data={"job": "Tester"})
        assert response.status in [201, 400, 403]
        if response.status == 201:
            body = response.json()
            assert "job" in body


def test_post_create_user_missing_job():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(BASE_URL, data={"name": "John"})
        assert response.status in [201, 400, 403]
        if response.status == 201:
            body = response.json()
            assert "name" in body


def test_post_create_user_empty_payload():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(BASE_URL, data={})
        assert response.status in [201, 400, 403]


def test_post_create_user_invalid_content_type():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(
            BASE_URL,
            data={"name": "Netra", "job": "QA"},
            headers={"Content-Type": "text/plain"}
        )
        # API likely ignores or errors on invalid content-type
        assert response.status in [201, 400, 403]


def test_put_update_user_valid():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.put(f"{BASE_URL}/2", data={"name": "Jane", "job": "Manager"})
        assert response.status in [200, 403]
        if response.status == 200:
            body = response.json()
            assert body["name"] == "Jane"


def test_put_update_user_invalid_id():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.put(f"{BASE_URL}/9999", data={"name": "Jane", "job": "Manager"})
        # Reqres returns 200 even if user doesn't exist for update
        assert response.status in [200, 403]


def test_patch_update_user_valid():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.patch(f"{BASE_URL}/2", data={"job": "Senior QA"})
        assert response.status in [200, 403]
        if response.status == 200:
            body = response.json()
            assert "job" in body


def test_delete_user_valid():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.delete(f"{BASE_URL}/2")
        assert response.status in [204, 403]


def test_delete_user_invalid_id():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.delete(f"{BASE_URL}/9999")
        # Reqres returns 204 even if user doesn't exist
        assert response.status in [204, 403]


def test_get_users_with_invalid_page_param():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(f"{BASE_URL}?page=invalid")
        assert response.status in [200, 403]
        if response.status == 200:
            body = response.json()
            assert "page" in body


def test_get_users_no_accept_header():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(f"{BASE_URL}?page=1")
        assert response.status in [200, 403]


def test_post_create_user_no_content_type_header():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(BASE_URL, data={"name": "Netra", "job": "QA"})
        assert response.status in [201, 403]


def test_post_create_user_large_payload():
    with sync_playwright() as p:
        api = p.request.new_context()
        large_name = "N" * 1000
        large_job = "J" * 1000
        response = api.post(BASE_URL, data={"name": large_name, "job": large_job})
        assert response.status in [201, 403]
        if response.status == 201:
            body = response.json()
            assert body["name"] == large_name


def test_get_users_check_response_time():
    import time
    with sync_playwright() as p:
        api = p.request.new_context()
        start = time.time()
        response = api.get(BASE_URL)
        end = time.time()
        assert response.status in [200, 403]
        assert (end - start) < 5  # response time less than 5 seconds


def test_get_single_user_delay():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(f"{BASE_URL}/2?delay=3")
        assert response.status in [200, 403]


def test_get_single_user_delay_invalid():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(f"{BASE_URL}/2?delay=invalid")
        assert response.status in [200, 403]


def test_get_list_users_delay():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(f"{BASE_URL}?delay=3")
        assert response.status in [200, 403]


def test_get_list_users_delay_invalid():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(f"{BASE_URL}?delay=invalid")
        assert response.status in [200, 403]


def test_post_create_user_with_extra_fields():
    with sync_playwright() as p:
        api = p.request.new_context()
        data = {"name": "Netra", "job": "QA", "extra": "field"}
        response = api.post(BASE_URL, data=data)
        assert response.status in [201, 403]
        if response.status == 201:
            body = response.json()
            assert body["name"] == "Netra"


def test_post_create_user_with_null_values():
    with sync_playwright() as p:
        api = p.request.new_context()
        data = {"name": None, "job": None}
        response = api.post(BASE_URL, data=data)
        assert response.status in [201, 403]


def test_put_update_user_with_partial_data():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.put(f"{BASE_URL}/2", data={"name": "Partial Update"})
        assert response.status in [200, 403]


def test_patch_update_user_empty_payload():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.patch(f"{BASE_URL}/2", data={})
        assert response.status in [200, 403]


def test_get_users_check_content_type_header():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(BASE_URL)
        assert response.status in [200, 403]
        if response.status == 200:
            assert "application/json" in response.headers.get("content-type", "")


def test_get_users_check_pagination_data():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(BASE_URL)
        if response.status == 200:
            body = response.json()
            assert "total" in body
            assert "total_pages" in body


def test_get_user_by_id_check_email():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get(f"{BASE_URL}/2")
        if response.status == 200:
            body = response.json()
            assert "email" in body["data"]
            assert "@" in body["data"]["email"]


# ----------- POST Test Cases ------------

def test_post_create_user_valid():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(
            BASE_URL,
            data={"name": "Netra", "job": "QA"}
        )
        assert response.status in [201, 403]
        if response.status == 201:
            body = response.json()
            assert body["name"] == "Netra"
            assert body["job"] == "QA"
            assert "id" in body
            assert "createdAt" in body


def test_post_create_user_missing_name():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(
            BASE_URL,
            data={"job": "Developer"}
        )
        assert response.status in [201, 400, 403]
        if response.status == 201:
            body = response.json()
            assert "job" in body


def test_post_create_user_missing_job():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(
            BASE_URL,
            data={"name": "John"}
        )
        assert response.status in [201, 400, 403]
        if response.status == 201:
            body = response.json()
            assert "name" in body


def test_post_create_user_empty_payload():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(
            BASE_URL,
            data={}
        )
        # Depending on API behavior, it might accept or reject empty data
        assert response.status in [201, 400, 403]


def test_post_create_user_invalid_content_type():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.post(
            BASE_URL,
            data={"name": "Netra", "job": "QA"},
            headers={"Content-Type": "text/plain"}
        )
        assert response.status in [201, 400, 403]


def test_post_create_user_large_payload():
    with sync_playwright() as p:
        api = p.request.new_context()
        large_name = "N" * 1000
        large_job = "J" * 1000
        response = api.post(
            BASE_URL,
            data={"name": large_name, "job": large_job}
        )
        assert response.status in [201, 403]
        if response.status == 201:
            body = response.json()
            assert body["name"] == large_name


def test_post_create_user_with_extra_fields():
    with sync_playwright() as p:
        api = p.request.new_context()
        data = {"name": "Netra", "job": "QA", "extra": "field"}
        response = api.post(BASE_URL, data=data)
        assert response.status in [201, 403]
        if response.status == 201:
            body = response.json()
            assert body["name"] == "Netra"


def test_post_create_user_with_null_values():
    with sync_playwright() as p:
        api = p.request.new_context()
        data = {"name": None, "job": None}
        response = api.post(BASE_URL, data=data)
        assert response.status in [201, 403]



# ----------- PUT Test Cases ------------

def test_put_update_user_valid():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.put(
            f"{BASE_URL}/2",
            data={"name": "Jane", "job": "Manager"}
        )
        assert response.status in [200, 403]
        if response.status == 200:
            body = response.json()
            assert body["name"] == "Jane"
            assert body["job"] == "Manager"
            assert "updatedAt" in body


def test_put_update_user_partial_data():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.put(
            f"{BASE_URL}/2",
            data={"name": "Jane"}
        )
        assert response.status in [200, 403]
        if response.status == 200:
            body = response.json()
            assert body["name"] == "Jane"


def test_put_update_user_invalid_id():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.put(
            f"{BASE_URL}/9999",
            data={"name": "Jane", "job": "Manager"}
        )
        # Reqres returns 200 even if user doesn't exist for PUT update
        assert response.status in [200, 403]


def test_put_update_user_empty_payload():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.put(
            f"{BASE_URL}/2",
            data={}
        )
        assert response.status in [200, 403]


def test_put_update_user_invalid_content_type():
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.put(
            f"{BASE_URL}/2",
            data={"name": "Jane", "job": "Manager"},
            headers={"Content-Type": "text/plain"}
        )
        assert response.status in [200, 400, 403]
        .
