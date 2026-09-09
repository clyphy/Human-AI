import sys
from pydantic import create_model, BaseModel, ValidationError
from typing import Dict, Any, List, Type

class DynamicValidationSandbox:
    def _map_string_to_type(self, type_str: str) -> Type:
        type_map = {"int": int, "float": float, "str": str, "string": str, "bool": bool}
        return type_map.get(type_str.lower(), str)

    def generate_pydantic_model(self, model_name: str, field_definitions: Dict[str, str]) -> Type[BaseModel]:
        parsed_fields = {}
        for field_name, type_str in field_definitions.items():
            parsed_fields[field_name] = (self._map_string_to_type(type_str), ...)
        return create_model(model_name, **parsed_fields)

    def validate_dataset(self, data_payload: List[Dict[str, Any]], pydantic_model: Type[BaseModel], rules: List[str]) -> Dict[str, Any]:
        validated_records = []
        try:
            for idx, record in enumerate(data_payload):
                # Phase 1: Dynamic Pydantic Type Checks
                instance = pydantic_model(**record)
                validated_records.append(instance.model_dump())
        except ValidationError as val_err:
            return {"success": False, "error_stage": "PYDANTIC_TYPE_MISMATCH", "error": val_err.errors()}

        # Phase 2: Domain Business Rule Checks
        violations = []
        for idx, row in enumerate(validated_records):
            for rule in rules:
                if not eval(rule, {}, row):
                    violations.append(f"Record #{idx} broke rule: ({rule}) Context: {row}")
                    
        if violations:
            return {"success": False, "error_stage": "BUSINESS_RULE_VIOLATION", "error": violations}

        return {"success": True, "data": validated_records}

# --- RUN EXECUTION TEST ---
if __name__ == "__main__":
    sandbox = DynamicValidationSandbox()

    # Mock parameters retrieved from your ChromaDB knowledge base
    mock_fields = {"invoice_id": "int", "amount": "float", "vendor_email": "str"}
    mock_rules = ["amount >= 0.0", "'@' in vendor_email"]

    # Compile the operational structural model at runtime
    TargetModel = sandbox.generate_pydantic_model("TestInvoiceModel", mock_fields)
    print("🤖 Dynamic Pydantic Model compiled successfully.\n")

    # TEST CASE A: Completely Valid Mock Dataset
    valid_mock_data = [
        {"invoice_id": 4401, "amount": 250.75, "vendor_email": "billing@corp.com"},
        {"invoice_id": 4402, "amount": 0.0, "vendor_email": "dev@stripe.io"}
    ]
    
    print("🧪 Running Test Case A (Valid Data)...")
    res_a = sandbox.validate_dataset(valid_mock_data, TargetModel, mock_rules)
    print(f"Result Success: {res_a['success']}\n")

    # TEST CASE B: Malformed Data (Triggers Pydantic Type Mismatch)
    # Note: invoice_id is passed as an alphanumeric string instead of an int
    type_flaw_data = [
        {"invoice_id": "INV-X", "amount": 100.0, "vendor_email": "ops@vendor.net"}
    ]
    
    print("🧪 Running Test Case B (Type Flaw Data)...")
    res_b = sandbox.validate_dataset(type_flaw_data, TargetModel, mock_rules)
    print(f"Result Success: {res_b['success']}")
    print(f"Stage: {res_b.get('error_stage')}")
    print(f"Details: {res_b.get('error')}\n")

    # TEST CASE C: Malformed Data (Triggers Business Rule Violation)
    # Note: Types match, but amount is negative and email is missing an '@'
    rule_flaw_data = [
        {"invoice_id": 4403, "amount": -15.50, "vendor_email": "invalid_email_string"}
    ]
    
    print("🧪 Running Test Case C (Rule Flaw Data)...")
    res_c = sandbox.validate_dataset(rule_flaw_data, TargetModel, mock_rules)
    print(f"Result Success: {res_c['success']}")
    print(f"Stage: {res_c.get('error_stage')}")
    print(f"Details: {res_c.get('error')}")
