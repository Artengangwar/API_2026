# Beginner's Guide to API Testing

## 📚 What You Need to Know

### 1. **What are API Tests?**
API tests check whether a web service works correctly. Instead of clicking buttons in a browser, we send requests (GET, POST, PUT, DELETE) and verify the responses.

### 2. **HTTP Methods (CRUD Operations)**

| Method | Action | Example |
|--------|--------|---------|
| **GET** | Retrieve data | Get a list of users |
| **POST** | Create new data | Create a new user |
| **PUT** | Update all fields | Replace user data completely |
| **PATCH** | Update some fields | Update only the job field |
| **DELETE** | Remove data | Delete a user |

### 3. **HTTP Status Codes**

| Code | Meaning |
|------|---------|
| **200** | OK - Request successful |
| **201** | Created - New resource created |
| **204** | No Content - Success but no response body |
| **400** | Bad Request - Invalid data sent |
| **403** | Forbidden - API blocked access |
| **404** | Not Found - Resource doesn't exist |

---

## 🧪 How to Use These Tests

### **Installation (First Time Setup)**

```bash
pip install playwright pytest
```

### **Run All Tests**
```bash
pytest test_login.py -v
```

### **Run Specific Test**
```bash
pytest test_login.py::test_get_all_users -v
```

### **Run with Output (See Print Statements)**
```bash
pytest test_login.py -v -s
```

### **Run Only GET Tests**
```bash
pytest test_login.py -k "get" -v
```

---

## 📖 Understanding the Test Structure

### **Simple Pattern Breakdown**

Every test follows this 3-step pattern:

```python
def test_get_all_users():
    # STEP 1: Setup - Create API client
    p, api = create_api_client()
    
    # STEP 2: Action - Make API request
    response = api.get(BASE_URL)
    
    # STEP 3: Assert - Verify the result
    assert response.status in [200, 403]
    
    # CLEANUP: Stop the client
    p.stop()
```

---

## 🔍 GET Request Tests

### **Test 1: Get Users from Page 2**
```python
def test_get_users_on_page_2():
    p, api = create_api_client()
    response = api.get(f"{BASE_URL}?page=2")
    print(f"Status Code: {response.status}")
    assert response.status in [200, 403]
    p.stop()
```

**What's happening?**
1. Create API client
2. Request GET /users?page=2
3. Print the status code
4. Check if status is 200 (success) or 403 (blocked)
5. Close the client

---

## 📝 POST Request Tests

### **Test: Create a New User**
```python
def test_create_new_user():
    p, api = create_api_client()
    
    user_data = {
        "name": "Netra",
        "job": "QA Engineer"
    }
    
    response = api.post(BASE_URL, data=user_data)
    
    if response.status == 201:  # 201 = Created
        created_user = response.json()
        assert created_user["name"] == "Netra"
    else:
        assert response.status == 403
    
    p.stop()
```

**What's happening?**
1. Create user data (name + job)
2. Send POST request with that data
3. If successful (201), parse JSON and verify the data
4. If blocked (403), that's okay too

---

## ✏️ PUT Request Tests (Update Everything)

### **Test: Update User Information**
```python
def test_update_user():
    p, api = create_api_client()
    
    user_id = 2
    updated_data = {
        "name": "Jane Doe",
        "job": "Senior QA"
    }
    
    response = api.put(f"{BASE_URL}/{user_id}", data=updated_data)
    
    if response.status == 200:
        updated_user = response.json()
        assert updated_user["name"] == "Jane Doe"
    
    p.stop()
```

**Key Difference:** PUT replaces ALL fields

---

## 🔧 PATCH Request Tests (Update Specific Fields)

### **Test: Partially Update User**
```python
def test_partial_update_user():
    p, api = create_api_client()
    
    user_id = 2
    partial_data = {"job": "Lead QA"}  # Only update job
    
    response = api.patch(f"{BASE_URL}/{user_id}", data=partial_data)
    
    if response.status == 200:
        updated_user = response.json()
        assert "job" in updated_user
    
    p.stop()
```

**Key Difference:** PATCH only changes what you send

---

## 🗑️ DELETE Request Tests

### **Test: Delete a User**
```python
def test_delete_user():
    p, api = create_api_client()
    
    user_id = 2
    response = api.delete(f"{BASE_URL}/{user_id}")
    
    # 204 = Deleted successfully
    # 403 = API blocked
    assert response.status in [204, 403]
    
    p.stop()
```

---

## 💡 Key Concepts for Beginners

### **1. What is `assert`?**
It checks if something is true. If false, the test fails.

```python
assert 5 > 3  # ✅ True, test passes
assert 5 < 3  # ❌ False, test fails
```

### **2. What is `in`?**
Checks if a value exists in a list.

```python
assert response.status in [200, 403]
# Check if status is either 200 or 403
```

### **3. What is JSON?**
Data format that's easy to read:
```python
data = {
    "id": 1,
    "name": "John",
    "job": "QA"
}
```

### **4. What is f-string?**
Python way to insert variables into text:
```python
user_id = 2
url = f"{BASE_URL}/{user_id}"
# Results in: "https://reqres.in/api/users/2"
```

---

## 🐛 Debugging Tips

### **Print the Response to Debug**
```python
response = api.get(BASE_URL)
print(f"Status: {response.status}")
print(f"Body: {response.text()}")
print(f"Headers: {response.headers}")
```

### **Run Test with Output**
```bash
pytest test_login.py::test_get_all_users -v -s
# The -s flag shows all print statements
```

### **Run Only Failed Tests Again**
```bash
pytest test_login.py --lf
```

---

## ✅ Checklist to Understand Each Test

When you read a test, ask yourself:
- [ ] What HTTP method is used? (GET, POST, PUT, PATCH, DELETE)
- [ ] What data is being sent? (if any)
- [ ] What status code is expected?
- [ ] What part of the response is being verified?
- [ ] What should happen if the API is blocked?

---

## 📚 Additional Resources

- **Playwright Docs:** https://playwright.dev/python/
- **REST API Concepts:** https://www.restapitutorial.com/
- **Pytest Documentation:** https://docs.pytest.org/

---

## 🎯 Next Steps

1. Run the tests: `pytest test_login.py -v -s`
2. Modify a test to add print statements
3. Create your own simple test
4. Try testing different endpoints

Good luck! 🚀

