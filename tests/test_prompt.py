import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import build_prompt

class Dummy:
    pass

def test_event():
    d = Dummy()
    d.event = 'Gala'
    d.date = '2025-05-30'
    d.tone = 'upbeat'
    assert 'Gala' in build_prompt(d)
