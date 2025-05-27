from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ProjectScannerService:
    def __init__(self):
        self.project_root = Path(".").resolve()
        self.source_path = self.project_root / "src"

    def extract_project_metadata(self) -> dict:
        solution_path = self._find_solution_file()
        project_name = solution_path.stem
        root_namespace = project_name

        return {
            "project_name": project_name,
            "root_namespace": root_namespace,
            "source_path": "src/",
            "domain_path": self._detect_layer_path("Domain"),
            "application_path": self._detect_layer_path("Application"),
            "infrastructure_path": self._detect_layer_path("Infrastructure"),
            "interchange_path": self._detect_layer_path("Interchange"),
            "tests_path": self._detect_tests_path(project_name),
        }

    def _find_solution_file(self) -> Path:
        slns = list(self.source_path.glob("*.sln"))
        if not slns:
            raise FileNotFoundError("No .sln file found in src/")
        return slns[0]

    def _detect_tests_path(self, project_name: str) -> str:
        test_folder = self.source_path / f"{project_name}.Tests"
        if test_folder.exists():
            return str(test_folder.relative_to(self.project_root))

        # Fallback: look for *.csproj with "test" in name
        for csproj in self.source_path.rglob("*.csproj"):
            if "test" in csproj.stem.lower():
                return str(csproj.parent.relative_to(self.project_root))

        return "src/Tests"

    def _detect_layer_path(self, layer: str) -> str:
        """
        Detects the `layer` folder only inside the folder that matches the solution/project name.
        e.g., src/MyProject/Domain ✅
              src/SomeLib/Domain   ❌
        """
        project_name = self._find_solution_file().stem
        candidate = self.source_path / project_name / layer

        if candidate.is_dir() and not self._is_under_tests(candidate):
            return str(candidate.relative_to(self.project_root))

        raise FileNotFoundError(
            f"No valid `{layer}` folder found under src/{project_name}/")

    def _is_under_tests(self, path: Path) -> bool:
        return any(part.lower() in ["tests", "test"] for part in path.parts)
