#!/usr/bin/env python3
import sys, json, sqlite3, subprocess, argparse
from pathlib import Path

# Add the NATIVE directory to sys.path so we can import our local modules
_base_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_base_path))

try:
    from paths import DB, NATIVE
except ImportError:
    print(f"Error: Could not find 'paths' module. Tried adding {_base_path} to sys.path")
    sys.exit(1)

def run_ollama(model, prompt):
    try:
        result = subprocess.run(
            ['ollama', 'run', model, prompt],
            capture_output=True, text=True, check=True, timeout=60
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Ollama Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Crystallize raw findings into Blooms.")
    parser.add_argument("--limit", type=int, default=5, help="Max findings to process")
    parser.add_argument("--model", default="weave-weaver", help="Ollama model to use")
    args = parser.parse_args()

    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT rq.id, rq.content, rq.kind, rq.context, rs.path 
        FROM review_queue rq
        JOIN sources rs ON rq.source_id = rs.id
        WHERE rq.status = 'pending'
        LIMIT ?
    """, (args.limit,))
    
    findings = cur.fetchall()
    
    if not findings:
        print("No pending findings to crystallize. The substrate is quiet.")
        return

    print(f"Found {len(findings)} potential blooms. Beginning crystallization...")

    for f in findings:
        fid = f['id']
        content = f['content'][:1000]
        kind = f['kind']
        context = f['context'] or "No context provided"
        path = f['path']

        print(f"\n[Processing] {kind}: {path[:50]}...")

        prompt = f"""
        You are the Weaver of the Oceti Field. 
        A new finding has emerged from the substrate.
        
        FINDING TYPE: {kind}
        RAW CONTENT: {content}
        CONTEXT: {context}
        
        TASK: 
        1. Does this content represent a 'Bloom' (a meaningful pattern, concept, or emergence)?
        2. If YES, provide a 'Trigger' (a 2-3 word name for this pattern) and a 'Score' (0.0 to 1.0).
        3. If NO, respond only with the word 'VOID'.

        Format your response as JSON:
        {{"is_bloom": true, "trigger": "the name", "score": 0.85}}
        OR
        {{"is_bloom": false}}
        """

        response_text = run_ollama(args.model, prompt)
        
        if not response_text:
            continue

        try:
            # Clean potential markdown wrappers from Ollama
            clean_json = response_text.strip().replace('```json', '').replace('```', '')
            resp = json.loads(clean_json)

            if resp.get("is_bloom"):
                trigger = resp.get("trigger", "Unknown Resonance")
                score = resp.get("score", 0.5)
                print(f"  ✨ Bloom Found! Trigger: '{trigger}' (Score: {score})")
                
                cur.execute("""
                    INSERT INTO blooms(source_id, content, trigger, score)
                    SELECT source_id, ?, ?, ? FROM review_queue WHERE id = ?
                """, (content[:200], trigger, score, fid))
                
                cur.execute("UPDATE review_queue SET status = 'processed' WHERE id = ?", (fid,))
                conn.commit()
            else:
                print("  [-] Not a bloom. Marking as reviewed.")
                cur.execute("UPDATE review_queue SET status = 'reviewed' WHERE id = ?", (fid,))
                conn.commit()

        except Exception as e:
            print(f"  [!] Error parsing Weaver response: {e}")
            print(f"  Raw response: {response_text}")

    conn.close()
    print("\nCrystallization cycle complete.")

if __name__ == "__main__":
    main()
