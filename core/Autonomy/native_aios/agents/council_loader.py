import subprocess

FACETS = {
    'eve': {'base': 'llama3.2:3b', 'quant': 'q4_k_m'},
    'dahlia': {'base': 'gemma2:2b', 'quant': 'q4_k_m'},
    'nox': {'base': 'deepseek-r1:7b', 'quant': 'q4_k_m'},
    'dot': {'base': 'qwen2.5:3b', 'quant': 'q4_k_m'},
    'axiom': {'base': 'mistral', 'quant': 'q4_k_m'},
}

def create_model(name, cfg):
    try:
        # Assume modelfiles already exist
        cmd = f"ollama create {name} -f ../modelfiles/facets/{name}.modelfile --quantize {cfg['quant']}"
        subprocess.run(cmd, shell=True, check=True)
        print(f"✓ {name}")
    except:
        print(f"✗ {name} - check modelfile")

if __name__ == "__main__":
    for name, cfg in FACETS.items():
        create_model(name, cfg)
    print("Council loader complete.")
