import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Regex extractors: blooms/eureka, code, formulas, concepts, timestamps, metadata."""
import re, json, hashlib
from paths import CONFIG

CANON_TERMS = ["autonomy","affordance","affordances","resonance","resonances","practice",
    "dahlia","eve","clifton-mirror","oceti weave","oceti","mycelium","bridge engine",
    "e8 lattice","bloom","mediator","native aios","attuner","midwife","steward","weave"]
LEGACY_TERMS = json.loads((CONFIG/'terminology_canon.json').read_text())['legacy_terms_to_flag']

BLOOM_RE = re.compile(
    r'\b(bloom|blooms|eureka|aha|ah-ha|a-ha|breakthrough|clicked|it clicked|'
    r'unlock(?:ed)?|threshold|phase transition|coherence spike|ΔL|dL|'
    r'smile metric|it landed|origin point|milestone|revelation|signal)\b', re.I)
BLOOM_NEAR = re.compile(
    r'(i realized|we found|this is the bridge|this changes|remember this|'
    r'do not lose this|don\'t lose this|threshold|coherence|eureka|bloom)', re.I)
CODE_FENCE_RE = re.compile(r'```([A-Za-z0-9_+\-]*)\n([\s\S]*?)```')
CODE_LINE_RE = re.compile(
    r'^(?:#!\s*/\S+|\s*(?:def |class |function |const |let |var |fn |pub fn |'
    r'SELECT |CREATE TABLE |#!/bin/bash))', re.M)
FORMULA_RE = re.compile(r'^[A-Za-zψΨΔλΣπ_][A-Za-z0-9_{}\[\]()ΔψλΣπ, .\-*+/=<>]+\s*=\s*\S.+$', re.M)
FORMULA_SIG_RE = re.compile(r'(L\s*=\s*0\.5|C_n\s*=|ΔL\s*>=?\s*3|dL\s*>=?\s*3|ψ\s*=|E8|108\s*Hz|432|1\.618)')
TS_RE = re.compile(
    r'\b\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?\b'
    r'|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b'
    r'|\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b|\bDay\s+\d+\b')
HEADING_RE = re.compile(r'^#{1,6}\s+(.+)$', re.M)
HASHTAG_RE = re.compile(r'(?<![\w&])#([A-Za-z][A-Za-z0-9_\-]{2,})')

def hsh(s): return hashlib.sha256(s.encode('utf-8','ignore')).hexdigest()[:16]

def context_block(lines, idx, span=2):
    lo=max(0,idx-span); hi=min(len(lines),idx+span+1)
    return '\n'.join(lines[lo:hi])

def terminology_flags(text):
    low=text.lower(); return [t for t in LEGACY_TERMS if re.search(r'\b'+re.escape(t)+r'\b', low)]

def extract_blooms(text):
    out=[]; lines=text.splitlines()
    for m in BLOOM_RE.finditer(text):
        # find line index
        before=text[:m.start()]; ln=before.count('\n')
        ctx=context_block(lines,ln)
        score=1.0 + (0.5 if BLOOM_NEAR.search(ctx) else 0)
        score+= 0.5 if TS_RE.search(ctx) else 0
        score+= 0.5 if FORMULA_SIG_RE.search(ctx) else 0
        score+= 0.5 if CODE_LINE_RE.search(ctx) else 0
        out.append({'content':m.group(0),'trigger':m.group(1).lower(),'score':round(score,2),
                    'context':ctx,'line_start':ln+1,'line_end':ln+1})
    return out

def extract_code(text):
    out=[]
    for m in CODE_FENCE_RE.finditer(text):
        lang, body = m.group(1) or 'unknown', m.group(2)
        before=text[:m.start()]; ln=before.count('\n')
        out.append({'language':lang,'content':body,'content_hash':hsh(body),
                    'line_start':ln+1,'line_end':ln+body.count('\n')+1})
    for m in CODE_LINE_RE.finditer(text):
        before=text[:m.start()]; ln=before.count('\n')
        line=m.group(0)
        if not any(c['content_hash']==hsh(line) for c in out):
            out.append({'language':'inline','content':line,'content_hash':hsh(line),
                        'line_start':ln+1,'line_end':ln+1})
    return out

def extract_formulas(text):
    out=[]; seen=set(); lines=text.splitlines()
    EQ_SUB_RE = re.compile(r'[A-Za-zψΨΔλΣπ_][\w.\[\]{}()*+\-/=<>ΔψλΣπ ]*=[^,;\n]+')
    for m in FORMULA_SIG_RE.finditer(text):
        before=text[:m.start()]; ln=before.count('\n')
        if ln>=len(lines): continue
        line=lines[ln]
        sub=EQ_SUB_RE.search(line)
        content=(sub.group(0) if sub else line).strip()
        if content and content not in seen:
            seen.add(content)
            out.append({'content':content,'content_hash':hsh(content),'line_start':ln+1})
    return out

def extract_concepts(text):
    out=[]
    for m in HEADING_RE.finditer(text):
        term=m.group(1).strip()
        out.append({'term':term,'definition':None})
    for m in HASHTAG_RE.finditer(text):
        out.append({'term':m.group(1),'definition':None})
    low=text.lower()
    for t in CANON_TERMS:
        if t in low: out.append({'term':t,'definition':None})
    # dedupe preserving count
    agg={}
    for c in out:
        k=c['term'].lower(); agg.setdefault(k,0); agg[k]+=1
    return [{'term':k,'occurrence_count':v} for k,v in agg.items()]

def extract_timestamps(text):
    out=[]; seen=set()
    for m in TS_RE.finditer(text):
        raw=m.group(0)
        if raw in seen: continue
        seen.add(raw); before=text[:m.start()]; ln=before.count('\n')
        out.append({'raw':raw,'iso':None,'line':ln+1})
    return out

def extract_all(text):
    return {
        'blooms': extract_blooms(text),
        'code': extract_code(text),
        'formulas': extract_formulas(text),
        'concepts': extract_concepts(text),
        'timestamps': extract_timestamps(text),
        'terminology_flags': terminology_flags(text),
    }
