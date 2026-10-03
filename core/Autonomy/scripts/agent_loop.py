import sys
import io
import json
import traceback
from typing import Dict, Any, List, Type
from pydantic import create_model, BaseModel, ValidationError

# =====================================================================
# SYSTEM EVALUATION SANDBOX
# =====================================================================
class DynamicValidationSandbox:
    def _map_string_to_type(self, type_str: str) -> Type:
        type_map = {"int": int, "float": float, "str": str, "string": str, "bool": bool}
        return type_map.get(type_str.lower(), str)

    def generate_pydantic_model(self, model_name: str, field_definitions: Dict[str, str]) -> Type[BaseModel]:
        parsed_fields = {}
        for field_name, type_str in field_definitions.items():
            parsed_fields[field_name] = (self._map_string_to_type(type_str), ...)
        return create_model(model_name, **parsed_fields)

    def execute_and_validate(self, generated_code: str, pydantic_model: Type[BaseModel], rules: List[str]) -> Dict[str, Any]:
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        
        sandbox_globals = {}
        error_log = None
        data_payload = None
        
        try:
            exec(generated_code, sandbox_globals)
            data_payload = sandbox_globals.get("output_data")
        except Exception:
            error_log = f"Syntax/Runtime Exception:\n{traceback.format_exc()}"
        finally:
            sys.stdout = old_stdout

        if error_log:
            return {"success": False, "error_stage": "RUNTIME", "error": error_log}
        if not isinstance(data_payload, list):
            return {"success": False, "error_stage": "VALIDATION", "error": "Output data variable must be an array list structure."}

        # Dynamic Pydantic Validation (Type Checks)
        validated_records = []
        try:
            for idx, record in enumerate(data_payload):
                instance = pydantic_model(**record)
                validated_records.append(instance.model_dump())
        except ValidationError as val_err:
            # Map raw validation objects seamlessly into structural feedback matrices
            error_details = val_err.errors()
            formatted_issues = [f"Field '{err['loc'][0]}' failed check type '{err['type']}': {err['msg']} (Bad input value: {err.get('input')})" for err in error_details]
            return {
                "success": False,
                "error_stage": "PYDANTIC_TYPE_MISMATCH",
                "error": "\n".join(formatted_issues)
            }

        # Domain Evaluation Assertions (Business Logic Constraints)
        violations = []
        for idx, row in enumerate(validated_records):
            for rule in rules:
                if not eval(rule, {}, row):
                    violations.append(f"Row item index #{idx} broke rule violation condition: ({rule}) Context data -> {row}")
                    
        if violations:
            return {"success": False, "error_stage": "BUSINESS_RULE_VIOLATION", "error": "\n".join(violations)}

        return {"success": True, "data": validated_records}

# =====================================================================
# AI LOGIC ENGINE (Simulating an iterative LLM Code Generator)
# =====================================================================
class AgentLogicEngine:
    def __init__(self):
        self.generation_turn = 0

    def generate_code_block(self, feedback_log: str = None) -> str:
        self.generation_turn += 1
        
        if self.generation_turn == 1:
            return """
# Initial Generation - Breaks Pydantic type bounds (invoice_id is string string instead of integer)
output_data = [
    {"invoice_id": "INV-X", "amount": 100.0, "vendor_email": "ops@vendor.net"}
]
"""
        elif self.generation_turn == 2:
            return """
# Second Generation - Self-corrected types, but breaks business rule constraints (negative amount)
output_data = [
    {"invoice_id": 4401, "amount": -15.50, "vendor_email": "invalid_email_string"}
]
"""
        else:
            return """
# Final Iteration - Code fully conforms to schema constraints and vector logic
output_data = [
    {"invoice_id": 4401, "amount": 250.75, "vendor_email": "billing@corp.com"},
    {"invoice_id": 4402, "amount": 15.00, "vendor_email": "dev@stripe.io"}
]
"""

# =====================================================================
# ORCHESTRATION PIPELINE
# =====================================================================
if __name__ == "__main__":
    sandbox = DynamicValidationSandbox()
    ai_agent = AgentLogicEngine()

    # Rule definitions extracted via ChromaDB vector lookups
    kb_fields = {"invoice_id": "int", "amount": "float", "vendor_email": "str"}
    kb_rules = ["amount >= 0.0", "'@' in vendor_email"]

    TargetModel = sandbox.generate_pydantic_model("AutomatedInvoiceModel", kb_fields)
    feedback_context = "Initial execution state."
    max_refinement_loops = 3
    success = False

    print("🚀 Initializing Closed-Loop Refinement Pipeline Verification Execution...\n")

    for loop in range(1, max_refinement_loops + 1):
        print(f"--- [Refinement Interaction Loop #{loop}] ---")
        
        # 1. AI Logic Engine accepts feedback loop statements to wresonance system code blocks
        code_blueprint = ai_agent.generate_code_block(feedback_context)
        
        # 2. Run simulation sandbox execution routines
        pipeline_run = sandbox.execute_and_validate(code_blueprint, TargetModel, kb_rules)
        
        if pipeline_run["success"]:
            print("✅ Code generation sequence verified! Data matches all target structures cleanly.")
            print(json.dumps(pipeline_run["data"], indent=2))
            success = True
            break
        else:
            print(f"🛑 Validation Intercepted Stage: {pipeline_run['error_stage']}")
            print("📝 Sourcing error text definitions to pass into next AI iteration block:")
            print(f"{pipeline_run['error']}\n")
            
            # Formulate clear instructions to feed back into the AI agent loop context 
            feedback_context = f"Your previous code run failed at stage {pipeline_run['error_stage']}.\nErrors found:\n{pipeline_run['error']}"

    if not success:
        print("🚨 Self-correction engine safety bounds exceeded without convergence.")
