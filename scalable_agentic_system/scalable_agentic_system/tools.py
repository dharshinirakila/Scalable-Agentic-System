from typing import Any

def create_invoice(amount: float, currency: str = "USD") -> dict[str, Any]:
    if amount <= 0:
        raise ValueError("amount must be greater than 0")
    return {
        "status": "created",
        "invoice_id": "INV-DEMO-001",
        "amount": amount,
        "currency": currency,
    }

def get_sales_volume(start_date: str, end_date: str) -> dict[str, Any]:
    return {
        "status": "success",
        "start_date": start_date,
        "end_date": end_date,
        "total_sales_volume": 12500.75,
        "currency": "USD",
    }

def get_dispute(user_id: str) -> dict[str, Any]:
    return {
        "status": "success",
        "user_id": user_id,
        "open_dispute": user_id == "user_123",
        "dispute_id": "DSP-DEMO-001" if user_id == "user_123" else None,
    }

def validate_parameters(tool_name: str, parameters: dict[str, Any]) -> None:
    required = {
        "create_invoice": ["amount"],
        "get_sales_volume": ["start_date", "end_date"],
        "get_dispute": ["user_id"],
    }
    for key in required.get(tool_name, []):
        if key not in parameters or parameters[key] in (None, ""):
            raise ValueError(f"Missing required parameter: {key}")

TOOL_FUNCTIONS = {
    "create_invoice": create_invoice,
    "get_sales_volume": get_sales_volume,
    "get_dispute": get_dispute,
}
