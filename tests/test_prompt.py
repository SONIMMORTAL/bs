from main import build_prompt

class Dummy:
    pass

def test_event():
    d = Dummy()
    d.event = 'Gala'
    d.date = '2025-05-30'
    d.tone = 'upbeat'
    assert 'Gala' in build_prompt(d)
