"""Install the checked Calcifer asset using Python's standard library."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
PET_ID = 'calcifer-basic'


def checked_assets() -> tuple[bytes, dict]:
    checksums = json.loads((ROOT / 'checksums.json').read_text(encoding='utf-8'))
    for relative, expected in checksums['sha256'].items():
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError('Checksum entry points outside this package')
        if not re.fullmatch(r'[0-9a-f]{64}', expected):
            raise ValueError(f'Invalid SHA-256 for {relative}')
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Checksum mismatch: {relative}')
    sheet = (ROOT / 'assets' / 'spritesheet.png').read_bytes()
    if not 0 < len(sheet) <= 20 * 1024 * 1024:
        raise ValueError('Spritesheet exceeds the supported byte size')
    if sheet[:8] != b'\x89PNG\r\n\x1a\n' or sheet[12:16] != b'IHDR':
        raise ValueError('Spritesheet is not a PNG')
    width, height = struct.unpack('>II', sheet[16:24])
    if (width, height, sheet[24], sheet[25]) != (1536, 1872, 8, 6):
        raise ValueError('Expected a 1536x1872, 8-bit RGBA PNG')
    manifest = json.loads((ROOT / 'pet.json').read_text(encoding='utf-8'))
    if manifest.get('spriteVersionNumber') != 1 or manifest.get('spritesheetPath') != 'spritesheet.png':
        raise ValueError('Unsupported pet manifest')
    if not isinstance(manifest.get('displayName'), str) or not manifest['displayName'].strip():
        raise ValueError('Missing display name')
    return sheet, manifest


def install(codex_home: Path, *, dry_run: bool = False, force: bool = False) -> dict:
    sheet, manifest = checked_assets()
    codex_home = codex_home.expanduser().resolve()
    pets_root = codex_home / 'pets'
    destination = pets_root / PET_ID
    if pets_root.is_symlink() or destination.is_symlink():
        raise ValueError('Refusing to install through a pets directory symlink')
    if destination.exists() and not destination.is_dir():
        raise ValueError('Pet destination is not a directory')
    expected = {'spritesheet.png': sheet,
                'pet.json': (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')}
    if any((destination / name).is_symlink() for name in expected):
        raise ValueError('Refusing to install over symlinked pet files')
    identical = False
    if (destination / 'spritesheet.png').is_file() and (destination / 'pet.json').is_file():
        try:
            identical = ((destination / 'spritesheet.png').read_bytes() == sheet and
                         json.loads((destination / 'pet.json').read_text(encoding='utf-8')) == manifest)
        except (OSError, ValueError):
            identical = False
    if destination.exists() and not identical and not force:
        raise ValueError('A different pet already exists here; use --force to back it up and replace it')
    report = {'pet_id': f'custom:{PET_ID}', 'destination': str(destination),
              'dry_run': dry_run, 'already_identical': identical, 'backup': None}
    if dry_run or identical:
        return report
    if destination.exists():
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup = codex_home / 'pet-backups' / f'{PET_ID}-{stamp}'
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(destination, backup)
        report['backup'] = str(backup)
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in expected.items():
        target = destination / name
        if target.is_symlink():
            raise ValueError(f'Refusing to overwrite symlink: {target}')
        target.write_bytes(content)
    if any((destination / name).read_bytes() != content for name, content in expected.items()):
        raise RuntimeError('Installed bytes did not match the package')
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-home', type=Path,
                        default=Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex'))
    parser.add_argument('--dry-run', action='store_true', help='Validate without writing files')
    parser.add_argument('--force', action='store_true', help='Back up and replace a different existing pet')
    args = parser.parse_args()
    try:
        report = install(args.codex_home, dry_run=args.dry_run, force=args.force)
    except (OSError, ValueError, RuntimeError, KeyError, struct.error) as exc:
        print(f'Install failed: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=True, indent=2))
    if not args.dry_run:
        print('Open Settings > Mini & Pets > Refresh, then select Calcifer.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
