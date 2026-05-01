"""
Simple API Tests using Playwright
===================================

This file contains beginner-friendly test cases for testing APIs.
Each test is simple, clear, and well-commented.
"""

from playwright.sync_api import sync_playwright

# Configuration
BASE_URL = "https://reqres.in/api/users"


# ============== HELPER FUNCTION ==============
def test_simple_api_request():
    """
    Simple helper to show basic API testing pattern
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        response = api.get("https://reqres.in/api/users")
        return response


# ============== SIMPLE GET TESTS ==============

def test_get_users_on_page_2():
    """
    Test: Get list of users on page 2
    
    What it does:
    1. Make a GET request to fetch users from page 2
    2. Check if the response status is 200 (success)
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Make the API request
        response = api.get(f"{BASE_URL}?page=2")
        
        # Step 2: Print the response for debugging
        print("\n--- GET Page 2 ---")
        print(f"Status Code: {response.status}")
        print(f"Response Body: {response.text()[:200]}...")  # First 200 chars
        
        # Step 3: Verify the response status
        assert response.status == 200, f"Expected 200, got {response.status}"


def test_get_users_with_json_response():
    """
    Test: Get users and check JSON response
    
    What it does:
    1. Make a GET request to fetch users
    2. Parse the JSON response
    3. Check that page number is correct
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Make the API request
        response = api.get(f"{BASE_URL}?page=2")
        print(f"\n--- GET With JSON ---")
        print(f"Status Code: {response.status}")
        
        # Step 2: Verify successful response
        assert response.status == 200, f"Expected 200, got {response.status}"
        
        # Step 3: Parse and verify the data
        data = response.json()
        print(f"Page Number: {data['page']}")
        print(f"Total Users on Page: {len(data.get('data', []))}")
        
        # Verify the page is correct
        assert data["page"] == 2, "Page number should be 2"


def test_get_all_users():
    """
    Test: Get all users (default page)
    
    What it does:
    1. Get users without specifying a page (defaults to page 1)
    2. Verify request was successful
    3. Check that we got users data
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Make the request
        response = api.get(BASE_URL)
        print(f"\n--- GET All Users ---")
        print(f"Status Code: {response.status}")
        
        # Step 2: Verify success
        assert response.status == 200, f"Expected 200, got {response.status}"
        
        # Step 3: Check the response has data
        data = response.json()
        assert "data" in data, "Response should contain 'data'"
        assert "page" in data, "Response should contain 'page'"
        print(f"Total Users: {len(data['data'])}")
        print(f"Total Pages: {data.get('total_pages', 'N/A')}")


def test_get_user_by_id():
    """
    Test: Get a specific user by ID
    
    What it does:
    1. Request a specific user (ID = 2)
    2. Verify the response
    3. Check that the correct user ID is returned
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Request user with ID = 2
        user_id = 2
        response = api.get(f"{BASE_URL}/{user_id}")
        print(f"\n--- GET User By ID ({user_id}) ---")
        print(f"Status Code: {response.status}")
        
        # Step 2: Verify request
        assert response.status == 200, f"Expected 200, got {response.status}"
        
        # Step 3: Verify we got the right user
        data = response.json()
        returned_id = data["data"]["id"]
        returned_email = data["data"]["email"]
        print(f"User ID: {returned_id}")
        print(f"User Email: {returned_email}")
        assert returned_id == user_id, f"Expected ID {user_id}, got {returned_id}"


# ============== SIMPLE POST TESTS ==============

def test_create_new_user():
    """
    Test: Create a new user
    
    What it does:
    1. Send a POST request with user data (name and job)
    2. Check if user was created successfully
    3. Verify the response data matches what we sent
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Prepare the data for new user
        user_data = {
            "name": "Netra",
            "job": "QA Engineer"
        }
        
        # Step 2: Send POST request to create user
        response = api.post(BASE_URL, data=user_data)
        print(f"\n--- POST Create User ---")
        print(f"Status Code: {response.status}")
        
        # Step 3: Check if creation was successful
        assert response.status == 201, f"Expected 201, got {response.status}"
        
        # Verify the returned data
        created_user = response.json()
        print(f"User Created with ID: {created_user.get('id')}")
        print(f"Name: {created_user.get('name')}")
        print(f"Job: {created_user.get('job')}")
        
        assert created_user["name"] == user_data["name"]
        assert created_user["job"] == user_data["job"]
        assert "id" in created_user


def test_create_user_without_name():
    """
    Test: Try to create user without name field
    
    What it does:
    1. Send POST request with only 'job' field (missing 'name')
    2. Check how API handles incomplete data
    3. Data should still be created (API accepts it)
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Send incomplete data (no name)
        user_data = {"job": "Tester"}
        response = api.post(BASE_URL, data=user_data)
        print(f"\n--- POST Create User (Missing Name) ---")
        print(f"Status Code: {response.status}")
        
        # Step 2: ReqRes accepts it and returns 201
        assert response.status == 201, f"Expected 201, got {response.status}"
        
        created_user = response.json()
        print(f"Created User ID: {created_user.get('id')}")
        print(f"Job Field: {created_user.get('job')}")


# ============== SIMPLE PUT TESTS ==============

def test_update_user():
    """
    Test: Update an existing user
    
    What it does:
    1. Send a PUT request to update user with ID 2
    2. Change the user's name and job
    3. Verify the update was successful
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Prepare updated data
        user_id = 2
        updated_data = {
            "name": "Jane Doe",
            "job": "Senior QA"
        }
        
        # Step 2: Send PUT request to update
        response = api.put(f"{BASE_URL}/{user_id}", data=updated_data)
        print(f"\n--- PUT Update User ---")
        print(f"Status Code: {response.status}")
        
        # Step 3: Verify update
        assert response.status == 200, f"Expected 200, got {response.status}"
        
        updated_user = response.json()
        print(f"Updated Name: {updated_user.get('name')}")
        print(f"Updated Job: {updated_user.get('job')}")
        
        assert updated_user["name"] == updated_data["name"]
        assert updated_user["job"] == updated_data["job"]
        assert "updatedAt" in updated_user


# ============== SIMPLE PATCH TESTS ==============

def test_partial_update_user():
    """
    Test: Partially update a user (PATCH)
    
    What it does:
    1. Send a PATCH request to update only the job field
    2. Keep other fields unchanged
    3. Verify only the job was updated
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Prepare partial data (only job)
        user_id = 2
        partial_data = {"job": "Lead QA"}
        
        # Step 2: Send PATCH request
        response = api.patch(f"{BASE_URL}/{user_id}", data=partial_data)
        print(f"\n--- PATCH Partial Update ---")
        print(f"Status Code: {response.status}")
        
        # Step 3: Verify the update
        assert response.status == 200, f"Expected 200, got {response.status}"
        
        updated_user = response.json()
        print(f"Updated Job: {updated_user.get('job')}")
        print(f"Updated At: {updated_user.get('updatedAt')}")
        assert "job" in updated_user
        assert updated_user["job"] == partial_data["job"]


# ============== SIMPLE DELETE TESTS ==============

def test_delete_user():
    """
    Test: Delete a user
    
    What it does:
    1. Send a DELETE request for user with ID 2
    2. Check if deletion was successful
    3. Verify response status (204 = No Content)
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Send DELETE request
        user_id = 2
        response = api.delete(f"{BASE_URL}/{user_id}")
        print(f"\n--- DELETE User ---")
        print(f"Status Code: {response.status}")
        
        # Step 2: Verify deletion
        # 204 means deleted successfully (no content returned)
        assert response.status == 204, f"Expected 204, got {response.status}"
        
        print("✅ User deleted successfully!")


def test_delete_nonexistent_user():
    """
    Test: Try to delete a user that doesn't exist
    
    What it does:
    1. Try to delete user with ID 9999 (doesn't exist)
    2. Check API's response to deleting non-existent data
    3. Most APIs still return 204 for DELETE requests
    """
    with sync_playwright() as p:
        api = p.request.new_context()
        
        # Step 1: Try to delete non-existent user
        response = api.delete(f"{BASE_URL}/9999")
        print(f"\n--- DELETE Non-existent User ---")
        print(f"Status Code: {response.status}")
        
        # Step 2: Verify response
        # ReqRes returns 204 even for non-existent users
        assert response.status == 204, f"Expected 204, got {response.status}"
        print("✅ API handled deletion of non-existent user gracefully")



# ============== HOW TO RUN TESTS ==============
# 
# Run all tests:
#   pytest test_login.py -v
#
# Run a specific test:
#   pytest test_login.py::test_get_all_users -v
#
# Run with output:
#   pytest test_login.py -v -s

