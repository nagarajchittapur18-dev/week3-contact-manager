from contacts_manager import contacts, add_contact, validate_phone, validate_email

def test_phone_validation():
    assert validate_phone("9876543210")[0] == True
    assert validate_phone("123")[0] == False

def test_email_validation():
    assert validate_email("test@gmail.com") == True
    assert validate_email("wrongemail") == False

print("✔ All tests passed manually.")
