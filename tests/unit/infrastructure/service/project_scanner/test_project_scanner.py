import os
from pathlib import Path

import pytest

from infrastructure.services.project_metadata_service import ProjectMetadataService
from infrastructure.services.project_scanner_service import ProjectScannerService


def test_extract_project_metadata_with_nested_layers(fs):
    """
    GIVEN this structure:

    /project/
    └── src/
        ├── Orientera.sln
        ├── Orientera/
        │   ├── Domain/
        │   ├── Application/
        │   ├── Infrastructure/
        │   └── Interchange/
        └── Orientera.Tests/

    EXPECT metadata:
    {
        'source_path': 'src/',
        'tests_path': 'src/Orientera.Tests',
        'domain_path': 'src/Orientera/Domain',
        'application_path': 'src/Orientera/Application',
        'infrastructure_path': 'src/Orientera/Infrastructure',
        'interchange_path': 'src/Orientera/Interchange',
        'project_name': 'Orientera',
        'root_namespace': 'Orientera'
    }
    """

    fs.create_dir('/project/src/Orientera/Domain')
    fs.create_dir('/project/src/Orientera/Application')
    fs.create_dir('/project/src/Orientera/Infrastructure')
    fs.create_dir('/project/src/Orientera/Interchange')
    fs.create_dir('/project/src/Orientera.Tests')
    fs.create_file('/project/src/Orientera.sln')

    # Change cwd to /project to simulate running in project root
    os.chdir('/project')

    scanner = ProjectScannerService(ProjectMetadataService(workdir=Path("/project")))
    metadata = scanner.extract_project_metadata()

    assert metadata == {
        'project_root': '/project',
        'source_path': '/project/src',
        'domain_path': '/project/src/Orientera/Domain',
        'application_path': '/project/src/Orientera/Application',
        'infrastructure_path': '/project/src/Orientera/Infrastructure',
        'interchange_path': '/project/src/Orientera/Interchange',
        'tests_path': '/project/src/Orientera.Tests',
        'project_name': 'Orientera',
        'root_namespace': 'Orientera',
        'persistence_provider': 'OpenDdd',
        'database_provider': 'Postgres',
    }


def test_flat_layer_folders_are_ignored(fs):
    """
    GIVEN this structure:

    /project/
    └── src/
        ├── OpenDDD.sln
        ├── Domain/
        └── OpenDDD/
            └── Application/

    EXPECT domain_path to raise FileNotFoundError because src/Domain is flat (invalid).
    """

    fs = fs
    fs.create_dir('/project/src/Domain')  # ❌ Invalid flat structure
    fs.create_dir('/project/src/OpenDDD/Application')  # ✅ Valid
    fs.create_file('/project/src/OpenDDD.sln')

    os.chdir('/project')
    scanner = ProjectScannerService(ProjectMetadataService(workdir=Path("/project")))

    with pytest.raises(FileNotFoundError):
        _ = scanner._detect_layer_path("Domain")

    # But Application path should work
    application_path = scanner._detect_layer_path("Application")
    assert application_path == '/project/src/OpenDDD/Application'


def test_only_solution_named_project_is_used(fs):
    """
    GIVEN this structure:

    /project/
    └── src/
        ├── Orientera.sln
        ├── SomeLib/
        │   └── Domain/
        ├── HelperLib/
        │   └── Domain/
        └── Orientera/
            └── Domain/

    EXPECT domain_path to be 'src/Orientera/Domain' — only the folder matching the solution name is considered.
    """

    fs = fs
    fs.create_dir('/project/src/SomeLib/Domain')
    fs.create_dir('/project/src/HelperLib/Domain')
    fs.create_dir('/project/src/Orientera/Domain')
    fs.create_file('/project/src/Orientera.sln')

    os.chdir('/project')
    scanner = ProjectScannerService(ProjectMetadataService(workdir=Path("/project")))

    domain_path = scanner._detect_layer_path("Domain")
    assert domain_path == '/project/src/Orientera/Domain'


def test_extracts_provider_settings_from_correct_config_file(fs):
    """
    GIVEN this structure:

    /project/
    └── src/
        ├── Orientera.sln
        ├── Orientera/
        │   ├── Domain/
        │   ├── Application/
        │   ├── Infrastructure/
        │   ├── Interchange/
        │   ├── appsettings.json (contains valid OpenDDD config)
        ├── Orientera.Tests/
        │   ├── appsettings.json (should be ignored)
        ├── SomeLib/
        │   ├── appsettings.json (should be ignored)

    EXPECT:
    - PersistenceProvider and DatabaseProvider are loaded from Orientera/appsettings.json
    """

    # Required folders to satisfy layer detection
    fs.create_dir('/project/src/Orientera/Domain')
    fs.create_dir('/project/src/Orientera/Application')
    fs.create_dir('/project/src/Orientera/Infrastructure')
    fs.create_dir('/project/src/Orientera/Interchange')

    # Appsettings file to be read
    fs.create_file('/project/src/Orientera/appsettings.json', contents="""
    {
        "OpenDDD": {
            "PersistenceProvider": "EfCore",
            "DatabaseProvider": "Postgres"
        }
    }
    """)

    # Other noise folders/files
    fs.create_dir('/project/src/Orientera.Tests')
    fs.create_dir('/project/src/SomeLib')

    fs.create_file('/project/src/Orientera.Tests/appsettings.json', contents="""
    {
        "OpenDDD": {
            "PersistenceProvider": "OpenDdd",
            "DatabaseProvider": "SqlLite"
        }
    }
    """)

    fs.create_file('/project/src/SomeLib/appsettings.json', contents="""
    {
        "OpenDDD": {
            "PersistenceProvider": "OpenDdd",
            "DatabaseProvider": "Mongo"
        }
    }
    """)

    fs.create_file('/project/src/Orientera.sln')

    os.chdir('/project')
    scanner = ProjectScannerService(ProjectMetadataService(workdir=Path("/project")))
    metadata = scanner.extract_project_metadata()

    assert metadata["persistence_provider"] == "EfCore"
    assert metadata["database_provider"] == "Postgres"
