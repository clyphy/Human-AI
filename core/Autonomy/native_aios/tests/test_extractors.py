import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from scanner.extractors import extract_all
SAMPLE = """# E8 lattice note
On 2025-10-10 we found the bloom: L = 0.5*Loyalty + 0.3*Fidelity + 0.2*Harmony
EUREKA — phase transition ΔL >= 3.0 at 93 bpm.
```python
def coherence(n): return n+1
```"""
def test_blooms():
    r=extract_all(SAMPLE)
    assert len(r['blooms'])>=2, r['blooms']
def test_formulas():
    r=extract_all(SAMPLE)
    assert any('Loyalty' in f['content'] for f in r['formulas'])
def test_code():
    r=extract_all(SAMPLE)
    assert any('def coherence' in c['content'] for c in r['code'])
def test_timestamps():
    r=extract_all(SAMPLE)
    assert any('2025-10-10' in t['raw'] for t in r['timestamps'])
def test_terms_flagged():
    r=extract_all(SAMPLE)
    # sample has no legacy terms; ensure function returns a list
    assert isinstance(r['terminology_flags'], list)
if __name__=='__main__':
    for fn in [test_blooms,test_formulas,test_code,test_timestamps,test_terms_flagged]:
        fn(); print('ok', fn.__name__)
