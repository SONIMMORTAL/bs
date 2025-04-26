from main import build_prompt
class Dummy:
    pass
def test_event():
    d = Dummy()
    d.event = 'Gala'
    d.date = '2025-05-30'
    d.time = '12:00'
    d.tone = 'upbeat'
    assert 'Gala' in build_prompt(d)
