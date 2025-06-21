import pytest

from codius.di import container
from codius.domain.model.config.config import Config
from codius.graph.nodes import distill_intent


@pytest.mark.integration
def test_add_aggregate():
    state = {
        "summary": "No previous context.",
        "user_input": "Create an aggregate root named Order."
    }

    result = distill_intent(state)

    expected = [
        {
            "intent": "add_aggregate",
            "target": "Order",
            "methods": [],
            "properties": []
        }
    ]

    assert result["intent"] == expected


@pytest.mark.integration
def test_multiple_operations():
    state = {
        "summary": "",
        "user_input": "Create an aggregate named Product and a value object named Price with amount and currency."
    }

    result = distill_intent(state)

    expected = [
        {
            "intent": "add_aggregate",
            "target": "Product",
            "methods": [],
            "properties": []
        },
        {
            "intent": "add_value_object",
            "target": "Price",
            "properties": [
                {"name": "Amount", "type": "decimal"},
                {"name": "Currency", "type": "string"}
            ]
        }
    ]

    assert result["intent"] == expected


@pytest.mark.integration
def test_unsure_case():
    state = {
        "summary": "",
        "user_input": "Maybe do something with the user model?"
    }

    result = distill_intent(state)

    expected = [
        {
            "intent": "unsure"
        }
    ]

    assert result["intent"] == expected


@pytest.mark.integration
def test_error_on_invalid_openai_api_key(monkeypatch):
    config = container.resolve(Config)
    config.llm.openai.api_key = "sk-invalid"

    state = {
        "summary": "",
        "user_input": "Create an aggregate named Order."
    }

    result = distill_intent(state)

    # Assert that the fallback error intent is returned
    assert isinstance(result["intent"], dict)
    assert result["intent"].get("intent") == "error"

    # Optional: assert the error message content for clarity
    assert "incorrect api key" in result["intent"].get("error_message", "").lower() \
           or "authentication failed" in result["intent"].get("error_message", "").lower()


@pytest.mark.integration
def test_add_method_with_implementation_hint():
    state = {
        "summary": "",
        "user_input": "Add method CalculateTotal to order aggregate that sums up the total price of all items in the Order."
    }

    result = distill_intent(state)

    method = result["intent"][0]["method"]
    implementation = method.get("implementation", {})

    assert result["intent"][0]["intent"] == "add_aggregate_method"
    assert result["intent"][0]["target"] == "Order"
    assert method["name"] == "CalculateTotal"
    assert implementation["type"] == "generate"
    assert "sum" in (implementation.get("hint") or "").lower()


@pytest.mark.integration
def test_add_method_without_implementation_hint():
    state = {
        "summary": "",
        "user_input": "Add cancel method to order aggregate."
    }

    result = distill_intent(state)

    method = result["intent"][0]["method"]
    implementation = method.get("implementation", {})

    assert result["intent"][0]["intent"] == "add_aggregate_method"
    assert result["intent"][0]["target"] == "Order"
    assert method["name"] == "Cancel"
    assert implementation.get("type") == "generate"
