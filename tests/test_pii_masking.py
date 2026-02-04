from src.pii_masking import mask_card_py, mask_email_py

def test_mask_card_py():
    assert mask_card_py("4111111111111111") == "XXXX-XXXX-XXXX-1111"
    assert mask_card_py("1234") == "XXXX-XXXX-XXXX-1234"
    assert mask_card_py("12") is None
    assert mask_card_py(None) is None

def test_mask_email_py():
    assert mask_email_py("john.doe@gmail.com") == "j***@gmail.com"
    assert mask_email_py("a@x.com") == "a***@x.com"
    assert mask_email_py("not_an_email") is None
    assert mask_email_py(None) is None
