import sys as _s; from pathlib import Path as _P; _s.path.insert(0, str((_P(__file__).resolve()).parent.parent))
"""Ties extractors together; scores blooms; returns a unified findings list."""
from scanner.extractors import extract_all, hsh
def extract_findings(text):
    """Return list of {kind, content, score, context, line_start, line_end, terminology_flags}."""
    parts = extract_all(text)
    flags = parts['terminology_flags']
    out=[]
    for b in parts['blooms']:
        out.append({'kind':'bloom','content':b['content'],'score':b['score'],
                    'context':b['context'],'line_start':b['line_start'],'line_end':b['line_end'],
                    'terminology_flags':flags,'trigger':b.get('trigger')})
    for c in parts['code']:
        out.append({'kind':'code','content':c['content'],'score':1.0,'context':None,
                    'line_start':c['line_start'],'line_end':c['line_end'],
                    'terminology_flags':flags,'language':c.get('language'),
                    'content_hash':c.get('content_hash')})
    for f in parts['formulas']:
        out.append({'kind':'formula','content':f['content'],'score':2.0,'context':None,
                    'line_start':f['line_start'],'line_end':f['line_start'],
                    'terminology_flags':flags,'content_hash':f.get('content_hash')})
    for c in parts['concepts']:
        out.append({'kind':'concept','content':c['term'],'score':0.5,'context':None,
                    'line_start':None,'line_end':None,'terminology_flags':flags,
                    'occurrence_count':c.get('occurrence_count')})
    for t in parts['timestamps']:
        out.append({'kind':'timestamp','content':t['raw'],'score':0.3,'context':None,
                    'line_start':t['line'],'line_end':t['line'],'terminology_flags':flags})
    return out, flags
