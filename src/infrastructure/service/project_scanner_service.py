import xml.etree.ElementTree as ET
from pathlib import Path
import logging
from typing import List

logger = logging.getLogger(__name__)


class ProjectScannerService:
    def __init__(self):
        self.project_root = Path(".").resolve()

    def extract_project_namespace(self) -> str:
        candidates = []

        for csproj in self.project_root.rglob("*.csproj"):
            name = csproj.stem.lower()
            if "test" in name:
                continue  # skip test projects

            try:
                tree = ET.parse(csproj)
                root = tree.getroot()
                ns_tag = root.find(".//RootNamespace")
                if ns_tag is not None and ns_tag.text:
                    candidates.append(ns_tag.text.strip())
                else:
                    candidates.append(csproj.stem)
            except Exception as e:
                logger.warning("Failed to parse %s: %s", csproj, e)

        if not candidates:
            return "MyProject"

        return self._shortest_shared_prefix(candidates)

    def _shortest_shared_prefix(self, namespaces: List[str]) -> str:
        if not namespaces:
            return "MyProject"

        # Split each namespace into parts
        split = [ns.split('.') for ns in namespaces]
        common = []

        for parts in zip(*split):
            if all(p == parts[0] for p in parts):
                common.append(parts[0])
            else:
                break

        return '.'.join(common) if common else namespaces[0]
