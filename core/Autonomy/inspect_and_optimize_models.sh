#!/bin/bash
cd ~/projects/Human-AI/core/Autonomy

echo "=== Ollama Model Inspection & Optimization Batch ==="
echo "Started: $(date)"
echo "Working directory: $(pwd)"
echo "==================================================="

mkdir -p modelfiles optimized

echo "Listing all installed models..."
ollama list

echo -e "\n=== Extracting details from all models ===\n"

for model in $(ollama list | tail -n +2 | awk '{print $1}'); do
    clean_name=$(echo $model | tr ':' '_' | tr '/' '_')
    
    echo "Processing: $model"
    
    echo "→ Saving full Modelfile..."
    ollama show "$model" --modelfile > "modelfiles/Modelfile.$clean_name" 2>/dev/null
    
    echo "→ System prompt:"
    ollama show "$model" --system 2>/dev/null || echo "   (none)"
    
    echo "→ Parameters:"
    ollama show "$model" --parameters 2>/dev/null || echo "   (none)"
    echo "─────────────────────────────────────"
done

echo -e "\n✅ All current models inspected and saved to modelfiles/ folder."
echo "You can now review them and create optimized versions."
echo "Run the next script when you're ready to create tuned versions."
