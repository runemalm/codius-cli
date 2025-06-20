import pytest
import difflib
from graph.nodes.generate_code import generate_code


@pytest.mark.integration
def test_generate_create_file(tmp_path):
    project_root = tmp_path / "project"
    project_root.mkdir(parents=True, exist_ok=True)

    file_plan = {
        "type": "create_file",
        "path": str(project_root / "Domain/Model/Invoice/Invoice.cs"),
        "template": "aggregate_root",
        "context": {
            "AggregateName": "Invoice",
            "Namespace": "MyApp.Domain.Model.Invoice",
            "Properties": [],
            "Events": [],
            "Commands": []
        },
        "description": "Create Invoice aggregate"
    }

    state = {
        "plan": [file_plan],
        "project_metadata": {
            "project_root": str(project_root)
        }
    }

    result = generate_code(state)

    assert "generated_files" in result
    assert any("Invoice.cs" in file["path"] for file in result["generated_files"])


@pytest.mark.integration
def test_generate_modify_file_with_add_method(tmp_path):
    # Arrange: original source file
    source_path = tmp_path / "Domain/Model/Invoice/Invoice.cs"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("""
using System;

namespace MyApp.Domain.Model.Invoice
{
    public class Invoice
    {
        public void RegisterPayment() {}
    }
}
""")

    file_plan = {
        "type": "modify_file",
        "path": str(source_path),
        "modification": "add_method",
        "context": {
            "aggregate_name": "Invoice",
            "method": {
                "name": "CalculateBalance",
                "parameters": [],
                "returns": "decimal",
                "body": "return Total - Payments.Sum();"
            },
            "placement": {
                "type": "after_method",
                "reference": "RegisterPayment"
            }
        },
        "description": "Add CalculateBalance method"
    }

    state = {
        "plan": [file_plan],
        "project_metadata": {
            "project_root": str(tmp_path)
        }
    }

    # Act
    result = generate_code(state)

    print("Generated files:", [f["path"] for f in result["generated_files"]])

    # Assert
    assert "generated_files" in result
    modified = next(f for f in result["generated_files"] if f["path"].endswith("Invoice.cs"))
    actual_content = modified["content"].strip()

    expected_content = """\
using System;

namespace MyApp.Domain.Model.Invoice
{
    public class Invoice
    {
        public void RegisterPayment() {}

        public decimal CalculateBalance()
        {
            return Total - Payments.Sum();
        }
    }
}
""".strip()

    if actual_content != expected_content:
        diff = "\n".join(difflib.unified_diff(
            expected_content.splitlines(),
            actual_content.splitlines(),
            fromfile='expected',
            tofile='actual',
            lineterm=''
        ))
        print("DIFF:\n" + diff)
        assert False, "Generated content does not match expected output."

    assert actual_content == expected_content


@pytest.mark.integration
def test_generate_modify_file_with_add_property(tmp_path):
    # Arrange: original source file
    source_path = tmp_path / "Domain/Model/Invoice/Invoice.cs"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text("""
using System;

namespace MyApp.Domain.Model.Invoice
{
    public class Invoice
    {
    }
}
""")

    file_plan = {
        "type": "modify_file",
        "path": str(source_path),
        "modification": "add_property",
        "context": {
            "aggregate_name": "Invoice",
            "property": {
                "type": "decimal",
                "name": "Total",
                "default": "0m"
            }
        },
        "description": "Add Total property"
    }

    state = {
        "plan": [file_plan],
        "project_metadata": {
            "project_root": str(tmp_path)
        }
    }

    # Act
    result = generate_code(state)

    print("Generated files:", [f["path"] for f in result["generated_files"]])

    # Assert
    assert "generated_files" in result
    modified = next(f for f in result["generated_files"] if f["path"].endswith("Invoice.cs"))
    actual_content = modified["content"].strip()

    expected_content = """\
using System;

namespace MyApp.Domain.Model.Invoice
{
    public class Invoice
    {
        public decimal Total { get; set; } = 0m;
    }
}
""".strip()

    if actual_content != expected_content:
        diff = "\n".join(difflib.unified_diff(
            expected_content.splitlines(),
            actual_content.splitlines(),
            fromfile='expected',
            tofile='actual',
            lineterm=''
        ))
        print("DIFF:\n" + diff)
        assert False, "Generated content does not match expected output."

    assert actual_content == expected_content
