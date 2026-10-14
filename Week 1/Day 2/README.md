# Week 1: Python and Project Foundation — Day 02

This repository tracks the foundational setup, validation logic, and decoupled business services for the backend development internship. 

---

## 📋 Business Rules & Validation Matrix (Rule Table)

| Field | Input Type | Enforced Business Rule | Valid Examples | Invalid Examples | Action on Failure |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Title** | `str` | Must be text, non-empty, no pure whitespace, max 100 characters. Returns stripped text. | `"Subodh Nepal"`, `"  Subodh Nepal "` | `""`, `"   "`, `"A" * 101`, `123` | Raises `ValidationError` |
| **Priority** | `int` / `str` | Must parse cleanly to an integer between 1 (Low) and 3 (High). | `1`, `"2"`, `3` | `0`, `4`, `"Task complete"`, `[]` | Raises `ValidationError` |

### Why Parsing is Different from Accepting
* **Accepting** checks only the primitive variable type signature (e.g., confirming an input is a string) without evaluating inner values. This allows dirty data like pure empty white spaces (`"   "`) to bypass security.
* **Parsing** actively checks formatting rules, sanitizes input noise (like running `.strip()`), and transforms data into valid domain types (like casting `"3"` to `3`) at the boundary layer.

---

## 💻 Technical Implementation (`validators.py`)

```python
class ValidationError(Exception):
    pass


def validate_title(title):
    if not isinstance(title, str):
        raise ValidationError("Title must be a string.")
    sanity_title = title.strip()
    if not sanity_title:
        raise ValidationError("Title cannot be empty or whitespace.")
    if len(sanity_title) > 100:
        raise ValidationError("Title cannot exceed 100 characters.")
    return sanity_title


def validate_priority(priority):
    try:
        priority = int(priority)
    except (ValueError, TypeError):
        raise ValidationError("Priority cannot be integer.")
    if priority not in:
        raise ValidationError("Priority should be 1, 2 or 3.")
    return priority


if __name__ == "__main__":
    try:
        assert validate_title("           Subodh Nepal  ") == "Subodh Nepal"
        assert validate_title("Subodh Nepal") == "Subodh Nepal"
        assert validate_priority(1) == 1
        assert validate_priority(2) == 2
        assert validate_priority(3) == 3

        print("All tests passed.")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        validate_title("   ")
        raise AssertionError("Empty title test failed.")
    except ValidationError:
        print("Empty title test passed.")

    try:
        validate_title("A" * 101)
        raise AssertionError("Long title test failed.")
    except ValidationError:
        print("Long title test passed.")

    try:
        validate_priority(4)
        raise AssertionError("Invalid priority test failed.")
    except ValidationError:
        print("Invalid priority test passed.")

    print("Test pass")
    print("Day 2 done")

    print("Breaking 1 rule")
    validate_priority("Task complete")
```

---

## 🔍 Verification & Acceptance Check (Sample Output)

Run the module directly from your terminal to trigger your self-contained assertions suite:

```bash
python -m app.validators
```

### Expected Console Output Trace:
```text
All tests passed.
Empty title test passed.
Long title test passed.
Invalid priority test passed.
Test pass
Day 2 done
Breaking 1 rule
Traceback (most recent call last):
  File "app/validators.py", line 51, in <module>
    validate_priority("Task complete")
  File "app/validators.py", line 16, in validate_priority
    raise ValidationError("Priority cannot be integer.")
__main__.ValidationError: Priority cannot be integer.
```
