import pytest

from infrastructure.services.code_scanner.code_scanner_service import CodeScannerService
from infrastructure.services.code_scanner.model.building_block import BuildingBlock
from infrastructure.services.code_scanner.model.building_block_type import BuildingBlockType


@pytest.mark.usefixtures("fs")
def test_scan_building_blocks_returns_correct_output(fs):
    # --- Arrange ---
    fs.create_dir("/project/src/Bookstore/Domain/Model/Book")
    fs.create_dir("/project/src/Bookstore/Application")
    fs.create_dir("/project/src/Bookstore/Infrastructure")

    # AggregateRoot: Book
    fs.create_file("/project/src/Bookstore/Domain/Model/Book/Book.cs", contents="""
using OpenDDD.Domain.Model.Base;

namespace Bookstore.Domain.Model.Book
{
    public class Book : AggregateRootBase<Guid>
    {
        public string Title { get; private set; }

        private Book() { }

        private Book(Guid id, string title) : base(id)
        {
            Title = title;
        }

        public static Book Create(string title)
        {
            return new Book(Guid.NewGuid(), title);
        }
    }
}
""")

    # AggregateRoot: Customer
    fs.create_file("/project/src/Bookstore/Domain/Customer.cs", contents="""
using OpenDDD.Domain.Model.Base;

namespace Bookstore.Domain
{
    public class Customer : AggregateRootBase<CustomerId>
    {
        public string Name { get; private set; }

        private Customer() { }

        private Customer(CustomerId id, string name) : base(id)
        {
            Name = name;
        }

        public static Customer Create(string name)
        {
            return new Customer(new CustomerId(), name);
        }
    }
}
""")

    # Other Domain Layer Files
    fs.create_file("/project/src/Bookstore/Domain/Model/IOrderRepository.cs", contents="""
namespace Bookstore.Domain;
public interface IOrderRepository {}
""")

    fs.create_file("/project/src/Bookstore/Domain/Model/CustomerRegistered.cs", contents="""
namespace Bookstore.Domain;
public class CustomerRegistered : IDomainEvent {}
""")

    fs.create_file("/project/src/Bookstore/Domain/Model/Ports/IEmailPort.cs", contents="""
namespace Bookstore.Domain.Ports;
public interface IEmailPort : IPort {}
""")

    # Application Layer Files
    fs.create_file("/project/src/Bookstore/Application/RegisterCustomerAction.cs", contents="""
namespace Bookstore.Application;
public class RegisterCustomerAction : IAction<RegisterCustomerCommand, Unit> {}
""")

    fs.create_file("/project/src/Bookstore/Application/RegisterCustomerCommand.cs", contents="""
namespace Bookstore.Application;
public class RegisterCustomerCommand : ICommand {}
""")

    fs.create_file("/project/src/Bookstore/Application/CustomerRegisteredListener.cs", contents="""
namespace Bookstore.Application;
public class CustomerRegisteredListener : EventListenerBase {}
""")

    fs.create_file("/project/src/Bookstore/Application/PersonUpdatedIntegrationEventListener.cs", contents="""
namespace Bookstore.Application;
public class PersonUpdatedIntegrationEventListener : EventListenerBase {}
""")

    # Infrastructure Layer Files
    fs.create_file("/project/src/Bookstore/Infrastructure/Adapters/Smtp/SmtpEmailAdapter.cs", contents="""
namespace Bookstore.Infrastructure.Adapters;
public class SmtpEmailAdapter : IEmailPort {}
""")

    # Project metadata mock
    metadata = {
        "project_name": "Bookstore",
        "root_namespace": "Bookstore",
        "project_root": "/project",
        "source_path": "/project/src",
        "domain_path": "/project/src/Bookstore/Domain",
        "application_path": "/project/src/Bookstore/Application",
        "infrastructure_path": "/project/src/Bookstore/Infrastructure",
        "interchange_path": "/project/src/Bookstore/Interchange",
        "tests_path": "/project/src/Bookstore.Tests",
    }

    scanner = CodeScannerService()

    # --- Act ---
    result = scanner.scan_building_blocks(metadata)

    # --- Assert ---
    assert isinstance(result, list)
    assert all(isinstance(bb, BuildingBlock) for bb in result)

    _assert_block_names(result, BuildingBlockType.AGGREGATE_ROOT, {"Book", "Customer"})
    _assert_block_names(result, BuildingBlockType.REPOSITORY, {"IOrderRepository"})
    _assert_block_names(result, BuildingBlockType.DOMAIN_EVENT, {"CustomerRegistered"})
    _assert_block_names(result, BuildingBlockType.PORT, {"IEmailPort"})
    _assert_block_names(result, BuildingBlockType.ACTION, {"RegisterCustomerAction"})
    _assert_block_names(result, BuildingBlockType.COMMAND, {"RegisterCustomerCommand"})
    _assert_block_names(result, BuildingBlockType.DOMAIN_EVENT_LISTENER, {"CustomerRegisteredListener"})
    _assert_block_names(result, BuildingBlockType.INTEGRATION_EVENT_LISTENER, {"PersonUpdatedIntegrationEventListener"})
    _assert_block_names(result, BuildingBlockType.ADAPTER, {"SmtpEmailAdapter"})


def _assert_block_names(result: list[BuildingBlock], block_type: BuildingBlockType, expected: set[str]):
    found = {bb.name for bb in result if bb.type == block_type}
    missing = expected - found
    extra = found - expected

    assert not missing, f"Missing {block_type.value.lower()}s: {missing}"
    assert not extra, f"Unexpected {block_type.value.lower()}s: {extra}"
