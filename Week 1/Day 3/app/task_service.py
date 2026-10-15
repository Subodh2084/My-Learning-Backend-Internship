class ValidationError(Exception):
    pass
#validationerror extending exception
#Title validation function is this
def validate_title(title):
    if not isinstance(title, str):
        raise ValidationError("Title must be a string.")
    sanity_title = title.strip()
    if not sanity_title:
        raise ValidationError("Title cannot be empty or whitespace.")
    if len(sanity_title) > 100:
        raise ValidationError("Title cannot exceed 100 characters.")
    return sanity_title
#validating priority (cannot be integer shoould be between 1 2 and 3)
def validate_priority(priority):
    try:
        priority = int(priority)
    except (ValueError, TypeError):
        raise ValidationError("Priority cannot be integer.")
    if priority not in [1,2,3]:
        raise ValidationError("Priority should be 1,2 or 3.")
    return priority;
if __name__ == "__main__":
    try:
        #checks for validation
        assert validate_title("           Subodh Nepal  ")=="Subodh Nepal"
        assert validate_title("Subodh Nepal")=="Subodh Nepal"
        assert validate_priority(1)==1
        assert validate_priority(2)==2
        assert validate_priority(3)==3

        print("All tests passed.")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    
    #raising problem for issue in validation
    
    try:
        validate_title("   ")
        raise AssertionError("Empty title test failed.")
    except ValidationError:
        print("Empty title test passed.")
    try:
        validate_title("A"*101)
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


