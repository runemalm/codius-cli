from pathlib import Path
from tree_sitter import Language, Parser, Tree


class TreeSitterService:
    def __init__(self):
        root = Path(__file__).resolve().parents[3]
        self.lib_path = root / "tree_sitter" / "build" / "my-languages.so"
        self.language_sources = [
            str(root / "tree_sitter" / "vendor" / "tree-sitter-c-sharp")
        ]
        self._language_cache = {}

    def ensure_languages_built(self):
        if not self.lib_path.exists():
            self.lib_path.parent.mkdir(parents=True, exist_ok=True)
            Language.build_library(str(self.lib_path), self.language_sources)

    def parse_code(self, source_code: str, language_name: str = "c_sharp") -> Tree:
        lang = self._get_language(language_name)
        parser = Parser()
        parser.set_language(lang)
        return parser.parse(source_code.encode("utf-8"))

    def _get_language(self, language_name: str) -> Language:
        self.ensure_languages_built()

        if language_name in self._language_cache:
            return self._language_cache[language_name]

        lang = Language(str(self.lib_path), language_name)
        self._language_cache[language_name] = lang
        return lang
