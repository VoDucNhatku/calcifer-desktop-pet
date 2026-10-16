"""Check real installation behavior in temporary Codex Home directories."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('pet_installer', ROOT / 'scripts' / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / 'codex-home'
            result = installer.install(home, dry_run=True)
            self.assertTrue(result['dry_run'])
            self.assertFalse(home.exists())

    def test_install_and_idempotent_reinstall(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            first = installer.install(home)
            self.assertFalse(first['already_identical'])
            pet = home / 'pets' / installer.PET_ID
            self.assertEqual((pet / 'spritesheet.png').read_bytes(),
                             (ROOT / 'assets' / 'spritesheet.png').read_bytes())
            before = (pet / 'spritesheet.png').stat().st_mtime_ns
            second = installer.install(home)
            self.assertTrue(second['already_identical'])
            self.assertEqual(before, (pet / 'spritesheet.png').stat().st_mtime_ns)

    def test_conflict_rejected_then_force_preserves_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            pet = home / 'pets' / installer.PET_ID
            pet.mkdir(parents=True)
            (pet / 'spritesheet.png').write_bytes(b'old pet bytes')
            (pet / 'pet.json').write_text('{}', encoding='utf-8')
            with self.assertRaises(ValueError):
                installer.install(home)
            self.assertEqual((pet / 'spritesheet.png').read_bytes(), b'old pet bytes')
            result = installer.install(home, force=True)
            self.assertEqual((Path(result['backup']) / 'spritesheet.png').read_bytes(), b'old pet bytes')
            self.assertEqual((pet / 'spritesheet.png').read_bytes(),
                             (ROOT / 'assets' / 'spritesheet.png').read_bytes())


if __name__ == '__main__':
    unittest.main()
