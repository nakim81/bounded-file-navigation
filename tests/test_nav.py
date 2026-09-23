import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'nav.py'


class NavigationTests(unittest.TestCase):
    def run_nav(self, root, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(root), *args],
                              capture_output=True, text=True)

    def test_truncation_and_narrowing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ('a', 'b', 'c'):
                (root / f'{name}.md').write_text('needle\n')
            result = self.run_nav(root, 'needle', '--mode', 'lines', '--limit', '1')
            self.assertEqual(result.returncode, 0)
            self.assertIn('a.md:1: needle', result.stdout)
            self.assertIn('TRUNCATED', result.stdout)
            result = self.run_nav(root, 'c.md', '--mode', 'paths')
            self.assertEqual(result.stdout.strip(), 'c.md')

    def test_exclusions_and_invalid_input(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'node_modules').mkdir()
            (root / 'node_modules' / 'hidden.md').write_text('secret-marker')
            self.assertIn('NO MATCH', self.run_nav(root, 'secret-marker', '--mode', 'lines').stdout)
            self.assertNotEqual(self.run_nav(root, '', '--limit', '0').returncode, 0)


if __name__ == '__main__':
    unittest.main()
