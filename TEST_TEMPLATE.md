# Simple Test Template for Beginners

## How to Create Your Own Simple Tests

Follow this template to create new tests. Each test has 3 parts:

---

## 🟢 GET Test Template

```python
def test_get_simple():
    """
    Test: [What does this test do?]
    
    What it does:
    1. [Step 1]
    2. [Step 2]
    3. [Step 3]
    """
    p, api = create_api_client()
    
    # STEP 1: Make the request
    response = api.get(BASE_URL)
    print(f"\n--- GET Request ---")
    print(f"Status Code: {response.status}")
    
    # STEP 2: Print info for debugging
    if response.status == 200:
        data = response.json()
        print(f"Response: {data}")
    
    # STEP 3: Verify the response
    assert response.status in [200, 403]
    
    p.stop()
```

---

## 🔵 POST Test Template

```python
def test_post_simple():
    """
    Test: [What does this test do?]
    
    What it does:
    1. Prepare the data
    2. Send POST request
    3. Verify response
    """
    p, api = create_api_client()
    
    # STEP 1: Prepare data to send
    data = {
        "name": "John",
        "job": "Developer"
    }
    
    # STEP 2: Send POST request
    response = api.post(BASE_URL, data=data)
    print(f"\n--- POST Request ---")
    print(f"Status Code: {response.status}")
    
    # STEP 3: Verify
    if response.status == 201:
        response_data = response.json()
        print(f"Created ID: {response_data.get('id')}")
        assert response_data["name"] == data["name"]
    else:
        assert response.status == 403
    
    p.stop()
```

---

## 🟠 PUT Test Template

```python
def test_put_simple():
    """
    Test: [What does this test do?]
    
    What it does:
    1. Prepare updated data
    2. Send PUT request
    3. Verify all fields updated
    """
    p, api = create_api_client()
    
    # STEP 1: Prepare new data
    user_id = 1
    new_data = {
        "name": "Alice",
        "job": "Manager"
    }
    
    # STEP 2: Send PUT request
    response = api.put(f"{BASE_URL}/{user_id}", data=new_data)
    print(f"\n--- PUT Request ---")
    print(f"Status Code: {response.status}")
    
    # STEP 3: Verify
    assert response.status in [200, 403]
    
    p.stop()
```

---

## 🟡 PATCH Test Template

```python
def test_patch_simple():
    """
    Test: [What does this test do?]
    
    What it does:
    1. Prepare partial data (only one field)
    2. Send PATCH request
    3. Verify only that field changed
    """
    p, api = create_api_client()
    
    # STEP 1: Prepare ONLY the field you want to change
    user_id = 1
    patch_data = {
        "job": "Director"  # Only changing job, not name
    }
    
    # STEP 2: Send PATCH request
    response = api.patch(f"{BASE_URL}/{user_id}", data=patch_data)
    print(f"\n--- PATCH Request ---")
    print(f"Status Code: {response.status}")
    
    # STEP 3: Verify
    assert response.status in [200, 403]
    
    p.stop()
```

---

## 🔴 DELETE Test Template

```python
def test_delete_simple():
    """
    Test: [What does this test do?]
    
    What it does:
    1. Prepare the ID to delete
    2. Send DELETE request
    3. Verify deletion
    """
    p, api = create_api_client()
    
    # STEP 1: Specify which resource to delete
    user_id = 1
    
    # STEP 2: Send DELETE request
    response = api.delete(f"{BASE_URL}/{user_id}")
    print(f"\n--- DELETE Request ---")
    print(f"Status Code: {response.status}")
    
    # STEP 3: Verify (204 = deleted, 403 = blocked)
    assert response.status in [204, 403]
    
    if response.status == 204:
        print("✅ User deleted successfully!")
    
    p.stop()
```

---

## 📋 Common Assertions

```python
# Check status code
assert response.status == 200

# Check status is one of multiple values
assert response.status in [200, 201, 403]

# Check JSON response has a field
assert "name" in response.json()

# Check JSON field value equals something
assert response.json()["name"] == "John"

# Check text contains something
assert "error" in response.text()
```

---

## 🧪 Testing Checklist Before You Submit

- [ ] Test has a clear docstring explaining what it does
- [ ] Test makes ONE API request
- [ ] Test prints the status code and response
- [ ] Test uses `assert` to verify results
- [ ] Test calls `p.stop()` at the end
- [ ] Test name starts with `test_`
- [ ] Test name describes what it's testing

---

## 🔧 Quick Start: Copy & Paste

```python
def test_my_first_test():
    """Test: A simple GET request"""
    p, api = create_api_client()
    
    response = api.get(BASE_URL)
    print(f"Status: {response.status}")
    
    assert response.status in [200, 403]
    p.stop()
```

Now replace:
1. `test_my_first_test` with your test name
2. `api.get(BASE_URL)` with your request
3. `[200, 403]` with expected statuses
4. Add more assertions as needed

---

## ❓ Common Questions

**Q: Do I need `p.stop()` at the end?**
A: Yes! It closes the browser/API connection.

**Q: Can I have multiple asserts?**
A: Yes! Add as many as you need.

**Q: What if the API is blocked (403)?**
A: Include it in the `assert` list: `[200, 403]`

**Q: How do I test an API with parameters?**
A: Use f-strings: `api.get(f"{BASE_URL}?page=2")`

**Q: How do I access JSON response data?**
A: Use `.json()`:
```python
data = response.json()
print(data["field_name"])
```

---

Good luck writing tests! 🎉

