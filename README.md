# 🎯 API Testing - Beginner Edition

Welcome! This is a beginner-friendly guide to testing APIs using Python and Playwright.

---

## 📂 What You Have

### Files in Your Project

```
ProjectP/
├── Tests/
│   └── test_login.py              ← Simple test cases (10 tests)
├── SUMMARY.md                      ← What changed & how to run
├── TESTING_GUIDE.md                ← Concepts & how to understand tests
├── TEST_TEMPLATE.md                ← How to write your own tests
└── README.md                       ← This file!
```

---

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
pip install pytest playwright
```

### Step 2: Run All Tests
```bash
pytest Tests/test_login.py -v -s
```

### Step 3: See the Results
You should see output like:
```
test_login.py::test_get_users_on_page_2 PASSED
test_login.py::test_get_all_users PASSED
test_login.py::test_create_new_user PASSED
... and more
```

---

## 📚 Understanding Your Tests

### What Are You Testing?
API calls to: `https://reqres.in/api/users`

This is a fake API for learning testing. It simulates:
- Creating users (POST)
- Reading users (GET)
- Updating users (PUT/PATCH)
- Deleting users (DELETE)

---

## 🧪 Your 10 Simple Tests

### GET Tests (Read Data)
1. **test_get_users_on_page_2** - Get a specific page of users
2. **test_get_users_with_json_response** - Parse JSON response
3. **test_get_all_users** - Get all users (default page)
4. **test_get_user_by_id** - Get one specific user

### POST Tests (Create Data)
5. **test_create_new_user** - Create a user successfully
6. **test_create_user_without_name** - Handle incomplete data

### PUT Test (Replace Data)
7. **test_update_user** - Update a user completely

### PATCH Test (Partial Update)
8. **test_partial_update_user** - Update just one field

### DELETE Tests (Remove Data)
9. **test_delete_user** - Delete a user
10. **test_delete_nonexistent_user** - Delete non-existent user

---

## 💡 The Simple Pattern

Every test follows this structure:

```python
def test_name():
    # 1️⃣ SETUP: Create API client
    p, api = create_api_client()
    
    # 2️⃣ ACTION: Make API request
    response = api.get(BASE_URL)
    
    # 3️⃣ VERIFY: Check the result
    assert response.status in [200, 403]
    
    # 🧹 CLEANUP: Stop client
    p.stop()
```

---

## 📋 Common Commands

### Run all tests with output
```bash
pytest Tests/test_login.py -v -s
```

### Run one specific test
```bash
pytest Tests/test_login.py::test_get_all_users -v -s
```

### Run only GET tests
```bash
pytest Tests/test_login.py -k "get" -v
```

### Run only POST tests
```bash
pytest Tests/test_login.py -k "post" -v
```

### Run failed tests again
```bash
pytest Tests/test_login.py --lf -v
```

### Run last 3 failed tests with output
```bash
pytest Tests/test_login.py --lf -v -s | head -20
```

---

## 🔍 Learning Path

### Week 1: Understand
- [ ] Read `SUMMARY.md` - Understand what changed
- [ ] Read `TESTING_GUIDE.md` - Learn API testing concepts
- [ ] Run all tests: `pytest Tests/test_login.py -v -s`
- [ ] Open `Tests/test_login.py` and read each test

### Week 2: Modify
- [ ] Change `test_get_users_on_page_2` to request page 3
- [ ] Add a print statement to `test_get_all_users`
- [ ] Run your modified tests
- [ ] Observe the output changes

### Week 3: Create
- [ ] Read `TEST_TEMPLATE.md`
- [ ] Create a new GET test using the template
- [ ] Create a new POST test
- [ ] Run your new tests

### Week 4: Expand
- [ ] Create PUT test
- [ ] Create PATCH test
- [ ] Create DELETE test
- [ ] Build your own test suite!

---

## 🧑‍💻 Example: Modify Your First Test

### Original Test
```python
def test_get_all_users():
    p, api = create_api_client()
    response = api.get(BASE_URL)
    print(f"Status Code: {response.status}")
    assert response.status in [200, 403]
    p.stop()
```

### Try This Modification
```python
def test_get_all_users():
    p, api = create_api_client()
    response = api.get(BASE_URL)
    print(f"Status Code: {response.status}")
    
    # ADD THESE LINES:
    if response.status == 200:
        data = response.json()
        print(f"Number of users: {len(data['data'])}")
        print(f"Page: {data['page']}")
    
    assert response.status in [200, 403]
    p.stop()
```

Then run:
```bash
pytest Tests/test_login.py::test_get_all_users -v -s
```

You'll see more information printed!

---

## 🤔 Understanding Key Concepts

### What is `assert`?
It checks if something is true. If false, the test fails.

```python
assert True   # ✅ Test passes
assert False  # ❌ Test fails
```

### What is `response.status`?
HTTP status code:
- **200** = Success ✅
- **201** = Created ✅
- **204** = Deleted ✅
- **400** = Bad request ❌
- **403** = Blocked ❌
- **404** = Not found ❌

### What is `response.json()`?
Converts response body to Python dictionary:
```python
response = api.get(BASE_URL)
data = response.json()  # Now it's a dict
print(data["name"])     # Access fields
```

### What is f-string?
Python way to put variables in text:
```python
name = "John"
print(f"Hello {name}")  # Prints: Hello John

page = 2
url = f"{BASE_URL}?page={page}"  # Inserts page number
```

---

## 🐛 Debugging

### See All Print Statements
```bash
pytest Tests/test_login.py -v -s
#                                   ^ This -s flag shows prints
```

### See Just Failed Tests
```bash
pytest Tests/test_login.py -v --tb=short
```

### See Full Error Details
```bash
pytest Tests/test_login.py -v --tb=long
```

### Stop At First Failure
```bash
pytest Tests/test_login.py -v -x
```

---

## ✨ File Descriptions

### `Tests/test_login.py`
Contains 10 simple test cases with:
- Clear docstrings
- Step-by-step comments
- Simple 3-step pattern
- Helper function for setup

### `TESTING_GUIDE.md`
Educational resource covering:
- API testing concepts
- HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Status codes
- How to run tests
- Debugging tips

### `TEST_TEMPLATE.md`
Template examples for writing tests:
- GET request template
- POST request template
- PUT request template
- PATCH request template
- DELETE request template
- Common assertions

### `SUMMARY.md`
Overview of changes:
- What improved
- Before/after comparison
- Quick start guide
- Test coverage

---

## 🎓 Key Learning Points

| Concept | Example |
|---------|---------|
| **GET** - Retrieve data | `api.get(BASE_URL)` |
| **POST** - Create data | `api.post(BASE_URL, data={...})` |
| **PUT** - Replace data | `api.put(f"{BASE_URL}/1", data={...})` |
| **PATCH** - Update field | `api.patch(f"{BASE_URL}/1", data={...})` |
| **DELETE** - Remove data | `api.delete(f"{BASE_URL}/1")` |
| **Status Codes** | 200=OK, 201=Created, 204=Deleted |
| **Assertions** | `assert value in [200, 403]` |
| **JSON** | `response.json()` to parse |

---

## 💼 What's Next?

### Option 1: Keep Learning
- Read all the guide files
- Modify existing tests
- Create new tests from template

### Option 2: Test More APIs
- Find another test API
- Adapt these tests for that API
- Keep practicing!

### Option 3: Go Deeper
- Learn about fixtures in pytest
- Learn about parameterized tests
- Learn about test reports

---

## ✅ Checklist to Get Started

- [ ] Install pytest: `pip install pytest`
- [ ] Install playwright: `pip install playwright`
- [ ] Run all tests: `pytest Tests/test_login.py -v -s`
- [ ] Read `TESTING_GUIDE.md`
- [ ] Read `TEST_TEMPLATE.md`
- [ ] Open `test_login.py` in your editor
- [ ] Read each test carefully
- [ ] Modify one test
- [ ] Create one new test

---

## 🆘 Troubleshooting

### Problem: "pytest: command not found"
**Solution:** Use `python -m pytest` instead
```bash
python -m pytest Tests/test_login.py -v
```

### Problem: "No module named playwright"
**Solution:** Install it
```bash
pip install playwright
```

### Problem: "Tests not found"
**Solution:** Check file paths
```bash
# Navigate to project root first
cd D:\Netra\ProjectP
pytest Tests/test_login.py -v
```

### Problem: "ModuleNotFoundError: No module named 'playwright'"
**Solution:** Make sure you're using the virtual environment
```bash
# Activate virtual environment first
.venv\Scripts\Activate.ps1  # Windows PowerShell
# Then install packages
pip install playwright pytest
```

---

## 📞 Need Help?

| Question | Answer |
|----------|--------|
| How do I run tests? | `pytest Tests/test_login.py -v` |
| How do I see output? | Add `-s` flag: `pytest Tests/test_login.py -v -s` |
| How do I see a specific test? | `pytest Tests/test_login.py::test_name -v -s` |
| How do I understand testing? | Read `TESTING_GUIDE.md` |
| How do I write my own test? | Read `TEST_TEMPLATE.md` |
| What changed? | Read `SUMMARY.md` |

---

## 🎉 You're Ready!

Your tests are:
- ✅ Simple and easy to read
- ✅ Well documented
- ✅ Ready to run
- ✅ Easy to modify
- ✅ Perfect for learning

### Next Step: Run this command 🚀
```bash
pytest Tests/test_login.py -v -s
```

Enjoy learning API testing! 🎓

---

## 📚 Extra Resources

- **Playwright Docs:** https://playwright.dev/python/
- **Pytest Docs:** https://docs.pytest.org/
- **REST API Tutorial:** https://www.restapitutorial.com/
- **HTTP Status Codes:** https://httpwg.org/specs/rfc7231.html#status.codes

---

*Last Updated: May 1, 2026*
*For Beginners in API Testing* 👨‍🎓👩‍🎓

