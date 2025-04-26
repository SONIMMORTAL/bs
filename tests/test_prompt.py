from main import build_prompt

class Dummy:
    pass

def test_event():
    d = Dummy()
    d.event = 'Gala'
    d.date = '2025-05-30'
    d.tone = 'upbeat'
    d.custom_prompt = None
    d.emails_only = False
    d.social_only = False
    d.email_count = 5
    d.social_count = 4
    d.additional_context = ""
    assert 'Gala' in build_prompt(d)
