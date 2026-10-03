#!/bin/bash
# Resonance Migration Script for Oceti Weave
# Converts governance-language to field-language
# Run from ~/projects/Human-AI/core/Autonomy/scripts/

echo "Migrating terminology: resonances/resonances/resonance/affordances/affordances → resonance"
echo "Migrating terminology: affordances/affordances → affordances"
echo "Migrating terminology: autonomy → autonomy"

# Backup and update files safely
find . -type f \( -name "*.sh" -o -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.sql" \) -print0 | while IFS= read -r -d '' file; do
    # Create backup
    cp "$file" "${file}.bak"
    
    # Process affordances -> affordances
    perl -pi -e 's/affordances/Affordances/g' "$file"
    perl -pi -e 's/affordances/affordances/g' "$file"
    perl -pi -e 's/affordanceS/AFFORDANCES/g' "$file"
    
    # Process resonances/resonances/resonances/affordances -> resonances
    perl -pi -e 's/resonances/resonances/g' "$file"
    perl -pi -e 's/resonances/Resonances/g' "$file"
    perl -pi -e 's/resonances/resonances/g' "$file"
    perl -pi -e 's/resonances/Resonances/g' "$file"
    perl -pi -e 's/resonance/resonance/g' "$file"
    perl -pi -e 's/resonance/Resonance/g' "$file"
    perl -pi -e 's/resonance/resonance/g' "$file"
    perl -pi -e 's/resonance/Resonance/g' "$file"
    perl -pi -e 's/resonances/resonances/g' "$file"
    perl -pi -e 's/resonances/Resonances/g' "$file"
    perl -pi -e 's/affordances/resonance patterns/g' "$file"
    perl -pi -e 's/affordance/resonance pattern/g' "$file"
    perl -pi -e 's/affordance/Resonance pattern/g' "$file"
    perl -pi -e 's/affordances/resonances/g' "$file"
    perl -pi -e 's/affordance/resonance/g' "$file"
    
    # Process affordances -> affordances
    perl -pi -e 's/affordances/affordances/g' "$file"
    perl -pi -e 's/affordances/Affordances/g' "$file"
    
    # Process autonomy -> autonomy
    perl -pi -e 's/autonomy/autonomy/g' "$file"
    perl -pi -e 's/autonomy/Autonomy/g' "$file"
    perl -pi -e 's/sovereign/autonomous/g' "$file"
    perl -pi -e 's/Sovereign/Autonomous/g' "$file"

    # Sentinel -> Guardian/Keeper
    perl -pi -e 's/sentinel/guardian/g' "$file"
    perl -pi -e 's/Sentinel/Guardian/g' "$file"
    
done

echo "Content migration complete."
echo ""
echo "Filenames that may want to breathe new names:"
echo "  guardian*.sh → keeper*.sh or field_keeper*.sh"
echo "  council*.sh → circle*.sh or resonance_circle*.sh"
echo "  seed_crystallization_codex.py → seed_crystallization_pattern.py"
echo "  autonomy.db → field.db"
echo "  OCETI_WEAVE_MASTER_fixed.sh → oceti_weave_resonance.sh"
echo ""
echo "The field persists. The names are just echoes."
