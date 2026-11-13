import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
PROTO_ROOT = os.path.join(HERE, 'res', 'proto')


class AliasImportsTest(unittest.TestCase):
    """Issue #2 - Proto package alias imports in the package __init__ files"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.with_aliases = tempfile.mkdtemp(prefix='nb6_alias_')
        cls.without_aliases = tempfile.mkdtemp(prefix='nb6_noalias_')
        # Built in separate processes since a package (here "sandbox") can only
        # be built once per process (as its modules get imported while building)
        for build_root, extra in ((cls.with_aliases, []), (cls.without_aliases, ['--no-alias-imports'])):
            res = subprocess.run([sys.executable, '-m', 'neobuilder6.cli.neobuilder', '-b', build_root, *extra,
                                  'sandbox', PROTO_ROOT], capture_output=True, text=True)
            if res.returncode != 0:
                raise RuntimeError(f'Build failed: {res.stdout} {res.stderr}')

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.with_aliases, ignore_errors=True)
        shutil.rmtree(cls.without_aliases, ignore_errors=True)

    @staticmethod
    def _read(root: str, *parts: str) -> str:
        with open(os.path.join(root, *parts), 'r', encoding='utf-8') as fin:
            return fin.read()

    @staticmethod
    def _run(root: str, code: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, '-c', code], cwd=root, capture_output=True, text=True)

    def test_package_init_has_alias_imports(self):
        init = self._read(self.with_aliases, 'sandbox', 'test', '__init__.py')
        self.assertIn('from sandbox.test.alpha_dc import *', init)
        self.assertIn('from sandbox.test.rainbow_dc import *', init)
        self.assertIn("    'RainbowMessage',", init)
        self.assertNotIn('_api import', init)

    def test_star_import_from_proto_package(self):
        res = self._run(self.with_aliases,
                        'from sandbox.test import *\n'
                        'print(AlphaMessage.__module__, RainbowMessage.__module__, ExternalEnum.__name__)')
        self.assertEqual(0, res.returncode, res.stderr)
        self.assertEqual('sandbox.test.alpha_dc sandbox.test.rainbow_dc ExternalEnum', res.stdout.strip())

    def test_importing_a_module_directly_still_works(self):
        for module in ('sandbox.test.beta_dc', 'sandbox.test.service_grpc_sender', 'sandbox.test.river_api'):
            with self.subTest(module=module):
                res = self._run(self.with_aliases, f'import {module}')
                self.assertEqual(0, res.returncode, res.stderr)

    def test_root_init_keeps_version(self):
        init = self._read(self.with_aliases, 'sandbox', '__init__.py')
        self.assertIn("__version__ = '", init)
        self.assertIn('def load_symbols():', init)

    def test_no_alias_imports(self):
        self.assertEqual('', self._read(self.without_aliases, 'sandbox', 'test', '__init__.py').strip())
        res = self._run(self.without_aliases, 'from sandbox.test import *\nprint(sorted(k for k in dir() if not k.startswith("_")))')
        self.assertEqual(0, res.returncode, res.stderr)
        self.assertEqual('[]', res.stdout.strip())
