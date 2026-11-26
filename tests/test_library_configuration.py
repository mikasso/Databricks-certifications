import ast
import contextlib
import io
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1] / "data-enginer associate cert"
NOTEBOOKS = (
    ROOT / "Includes" / "_common.py",
    ROOT / "Solutions" / "Includes" / "_common.py",
)


class FakeSparkError(Exception):
    def __init__(self, error_class):
        self.error_class = error_class

    def getErrorClass(self):
        return self.error_class


class FakeConf:
    def __init__(self, settings):
        self.settings = settings

    def get(self, key, default):
        value = self.settings.get(key, default)
        if isinstance(value, Exception):
            raise value
        return value


def load_installer(notebook, settings):
    tree = ast.parse(notebook.read_text(encoding="utf-8"), filename=str(notebook))
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name in ("__library_config", "__install_libraries")
    ]
    module = ast.Module(body=functions, type_ignores=[])
    namespace = {
        "PySparkException": FakeSparkError,
        "spark": types.SimpleNamespace(conf=FakeConf(settings)),
        "__validate_libraries": lambda: None,
    }
    exec(compile(module, str(notebook), "exec"), namespace)
    return namespace


class LibraryConfigurationTests(unittest.TestCase):
    def test_unavailable_settings_use_default_installation(self):
        for notebook in NOTEBOOKS:
            with self.subTest(notebook=notebook):
                unavailable = FakeSparkError("CONFIG_NOT_AVAILABLE.WITHOUT_SUGGESTION")
                installer = load_installer(notebook, {
                    "dbacademy.library.version": unavailable,
                    "dbacademy.library.install": unavailable,
                })
                output = io.StringIO()
                with patch.dict(sys.modules, {"dbacademy": types.ModuleType("dbacademy")}), \
                        contextlib.redirect_stdout(output):
                    installer["__install_libraries"]()
                self.assertIn("dbacademy-3.0.42-py3-none-any.whl", installer["pip_command"])
                self.assertIn("dbacademy.library.version", output.getvalue())
                self.assertIn("dbacademy.library.install", output.getvalue())

    def test_supported_overrides_are_used(self):
        for notebook in NOTEBOOKS:
            with self.subTest(notebook=notebook):
                installer = load_installer(notebook, {
                    "dbacademy.library.version": "v1.2.3",
                    "dbacademy.library.install": "install custom-package",
                })
                output = io.StringIO()
                with patch.dict(sys.modules, {"dbacademy": types.ModuleType("dbacademy")}), \
                        contextlib.redirect_stdout(output):
                    installer["__install_libraries"]()
                self.assertEqual(installer["pip_command"], "install custom-package")
                self.assertIn("v1.2.3", output.getvalue())

    def test_existing_matching_library_is_not_reinstalled(self):
        for notebook in NOTEBOOKS:
            with self.subTest(notebook=notebook):
                installer = load_installer(notebook, {})
                academy = types.ModuleType("dbacademy")
                academy.dbgems = types.SimpleNamespace(
                    lookup_current_module_version=lambda name: "v3.0.42"
                )
                with patch.dict(sys.modules, {"dbacademy": academy}):
                    installer["__install_libraries"]()
                self.assertEqual(installer["pip_command"], "list --quiet")

    def test_unrelated_errors_propagate_for_each_setting(self):
        for notebook in NOTEBOOKS:
            for key in ("dbacademy.library.version", "dbacademy.library.install"):
                with self.subTest(notebook=notebook, key=key):
                    error = FakeSparkError("OTHER_ERROR")
                    installer = load_installer(notebook, {key: error})
                    with patch.dict(sys.modules, {"dbacademy": types.ModuleType("dbacademy")}), \
                            self.assertRaises(FakeSparkError) as raised:
                        installer["__install_libraries"]()
                    self.assertIs(raised.exception, error)


if __name__ == "__main__":
    unittest.main()
