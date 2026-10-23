import sys

class ValidationError(Exception):
    
    pass

def validate_username(username: str) -> str:
    
    # 1. Type Boundary Check
    if not isinstance(username, str):
        raise TypeError(f"Input must be a string, got {type(username).__name__}")
        
    
    sanitized = username.strip()
    
    
    if len(sanitized) < 3:
        raise ValidationError("Username too short /3 chars minimum).")
        
    
    if len(sanitized) > 15:
        raise ValidationError("Username too long /15 chars maximum).")
        
    
    if not sanitized.isalnum():
        raise ValidationError("Username must be alphanumeric (no spaces, symbols, or special characters).")
        
    return sanitized.lower()


if __name__ == "__main__":
    print("--- Running Boundary Tests ---")
    
    tests = {
        "Valid Standard": "Alice123",
        "Exact Lower Limit (3)": "Bob",
        "Exact Upper Limit (15)": "User12345678901",
        "Below Lower Limit (2)": "Ed",
        "Above Upper Limit (16)": "User123456789012",
        "Empty String": "",
        "Whitespace Only": "   ",
        "Special Characters": "admin!",
        "Wrong Type (Int)": 12345
    }
    
    for test_name, value in tests.items():
        try:
            result = validate_username(value)
            print(result)
        except (ValidationError, TypeError) as e:
            print(e)
