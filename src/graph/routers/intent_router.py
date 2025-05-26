def route_by_intent(state: dict) -> str:
    intent_data = state.get("intent")

    if isinstance(intent_data, dict):
        intent_type = intent_data.get("intent", "").strip().lower()
        if intent_type and intent_type not in {"none", "greeting", "unsure"}:
            return "valid"

    return "unclear"
