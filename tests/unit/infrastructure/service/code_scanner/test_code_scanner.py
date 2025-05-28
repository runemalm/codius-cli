from pathlib import Path

from infrastructure.services.code_scanner.code_scanner import scan_building_blocks
from infrastructure.services.code_scanner.model.building_block import BuildingBlock
from infrastructure.services.code_scanner.model.building_block_type import BuildingBlockType


def test_scan_building_blocks_returns_expected_structure(project_path: Path):
    result = scan_building_blocks(project_path)

    assert isinstance(result, list), "Expected list of building blocks"
    assert all(isinstance(bb, BuildingBlock) for bb in result), "All elements should be BuildingBlock instances"

    _assert_block_names(
        result,
        BuildingBlockType.AGGREGATE_ROOT,
        expected={"Book", "Customer", "Order"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.ENTITY,
        expected={"LineItem"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.VALUE_OBJECT,
        expected={"Money"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.COMMAND,
        expected={"GetCustomerCommand", "GetCustomersCommand", "GetOrdersCommand", "PlaceOrderCommand", "RegisterCustomerCommand",
                  "SearchBooksCommand", "SendWelcomeEmailCommand", "UpdateCustomerNameCommand"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.ACTION,
        expected={"GetCustomerAction", "GetCustomersAction", "GetOrdersAction", "PlaceOrderAction", "RegisterCustomerAction",
                  "SearchBooksAction", "SendWelcomeEmailAction", "UpdateCustomerNameAction"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.DOMAIN_EVENT,
        expected={"CustomerRegistered"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.DOMAIN_EVENT_LISTENER,
        expected={"CustomerRegisteredListener"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.INTEGRATION_EVENT_LISTENER,
        expected={"PersonUpdatedIntegrationEventListener"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.INFRASTRUCTURE_SERVICE,
        expected=set()  # Add expected infrastructure services here if any
    )
    _assert_block_names(
        result,
        BuildingBlockType.ADAPTER,
        expected={"SmtpEmailAdapter", "ConsoleEmailAdapter"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.REPOSITORY,
        expected={"ICustomerRepository", "IOrderRepository"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.PORT,
        expected={"IEmailPort"}
    )
    _assert_block_names(
        result,
        BuildingBlockType.DOMAIN_SERVICE,
        expected={"ICustomerDomainService", "IOrderDomainService"}
    )


def _assert_block_names(result: list[BuildingBlock], block_type: BuildingBlockType, expected: set[str]):
    found = {bb.name for bb in result if bb.type == block_type}
    missing = expected - found
    extra = found - expected

    assert not missing, f"Missing {block_type.value.lower()}s: {missing}"
    assert not extra, f"Unexpected {block_type.value.lower()}s: {extra}"
