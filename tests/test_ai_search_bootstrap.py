"""Native CLI boundary is faked here; these are installer contract tests, NOT live E2E."""
import hashlib
import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'ai_search_bootstrap.py'
if SCRIPT.exists():
    spec = importlib.util.spec_from_file_location('bootstrap', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
else:
    module = None


def bundle(root):
    p = root / 'bundle'
    p.mkdir()
    files = {}
    for i in range(8):
        name = 'minora-test-' + str(i)
        rel = 'skills/' + name + '/SKILL.md'
        (p / rel).parent.mkdir(parents=True)
        content = f'---\nname: {name}\ndescription: Use when testing {i}.\n---\n# Test\n'
        (p / rel).write_text(content)
        files[rel] = hashlib.sha256(content.encode()).hexdigest()
    (p / 'manifest.json').write_text(json.dumps({'name': 'minora-ai-search-us', 'version': '0.1.0',
        'skills': ['minora-test-' + str(i) for i in range(8)], 'files': files}))
    return p


class Presence(unittest.TestCase):
    def test_installer_exists(self):
        self.assertTrue(SCRIPT.exists(), 'Missing safe Hermes installer')


@unittest.skipIf(module is None, 'Installer not implemented yet')
class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bundle = bundle(self.root)
        self.home = self.root / '.hermes'
        self.home.mkdir()
        (self.home / '.env').write_text('SENTINEL_ROOT_SECRET=do-not-copy')
        self.calls = []

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, args, env):
        self.calls.append(args)
        if args == ['profile', 'install', '--help']:
            return 0, '--name --yes --alias local directory'
        if args == ['--version']:
            return 0, 'Hermes Agent 0.19.0'
        if args[:2] == ['profile', 'install']:
            source = Path(args[2])
            destination = self.home / 'profiles' / 'minora-ai-search-us'
            destination.mkdir(parents=True)
            m = json.loads((source / 'distribution.yaml').read_text())
            for relative in m['distribution_owned']:
                src, dst = source / relative, destination / relative
                if src.is_dir():
                    shutil.copytree(src, dst)
                elif src.is_file():
                    shutil.copyfile(src, dst)
            return 0, 'installed'
        return 0, 'ok'

    def cli_with_native_metadata(self, args, env):
        result = self.cli(args, env)
        if args[:2] == ['profile', 'install'] and '--help' not in args:
            source = Path(args[2])
            installed = self.home / 'profiles/minora-ai-search-us/distribution.yaml'
            manifest = json.loads(installed.read_text())
            manifest.pop('env_requires')
            manifest['distribution_owned'] = [x.rstrip('/') for x in manifest['distribution_owned']]
            manifest['source'] = str(source)
            manifest['installed_at'] = '2026-09-20T10:31:02+00:00'
            installed.write_text(json.dumps(manifest))
        return result

    def run_install(self, apply=True, runner=None):
        return module.install(self.bundle, self.home, apply=apply, runner=runner or self.cli)

    def test_preview_does_not_modify_profile(self):
        r = self.run_install(False)
        self.assertEqual(r['status'], 'preview')
        self.assertFalse((self.home / 'profiles').exists())

    def test_fresh_install(self):
        r = self.run_install()
        self.assertEqual(r['status'], 'installed_requires_provider_and_live_checks')
        self.assertEqual(len(list((self.home / 'profiles/minora-ai-search-us/skills').glob('*/SKILL.md'))), 8)

    def test_native_distribution_metadata_rewrite_is_verified(self):
        r = self.run_install(runner=self.cli_with_native_metadata)
        self.assertEqual(r['status'], 'installed_requires_provider_and_live_checks')
        r = self.run_install(runner=self.cli_with_native_metadata)
        self.assertEqual(r['status'], 'already_installed')

    def test_wrong_native_distribution_source_is_refused(self):
        def wrong_source(args, env):
            result = self.cli_with_native_metadata(args, env)
            if args[:2] == ['profile', 'install'] and '--help' not in args:
                installed = self.home / 'profiles/minora-ai-search-us/distribution.yaml'
                manifest = json.loads(installed.read_text())
                manifest['source'] = '/unapproved/source'
                installed.write_text(json.dumps(manifest))
            return result
        with self.assertRaises(ValueError):
            self.run_install(runner=wrong_source)

    def test_installed_distribution_tampering_is_refused(self):
        self.run_install(runner=self.cli_with_native_metadata)
        installed = self.home / 'profiles/minora-ai-search-us/distribution.yaml'
        manifest = json.loads(installed.read_text())
        manifest['unexpected'] = 'value'
        installed.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            self.run_install(runner=self.cli_with_native_metadata)

    def test_receipt_cannot_hide_distribution_source_change(self):
        self.run_install(runner=self.cli_with_native_metadata)
        base = self.home / 'profiles/minora-ai-search-us'
        installed = base / 'distribution.yaml'
        manifest = json.loads(installed.read_text())
        manifest['source'] = '/unapproved/source'
        installed.write_text(json.dumps(manifest))
        receipt_path = base / '.minora-install.json'
        receipt = json.loads(receipt_path.read_text())
        receipt['distribution_source'] = '/unapproved/source'
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaises(ValueError):
            self.run_install(runner=self.cli_with_native_metadata)

    def test_receipt_version_change_is_refused(self):
        self.run_install()
        receipt_path = self.home / 'profiles/minora-ai-search-us/.minora-install.json'
        receipt = json.loads(receipt_path.read_text())
        receipt['version'] = '9.9.9'
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaises(ValueError):
            self.run_install()

    def test_no_secret_copy(self):
        self.run_install()
        p = self.home / 'profiles/minora-ai-search-us'
        self.assertFalse((p / '.env').exists())
        self.assertNotIn('do-not-copy', ''.join(f.read_text() for f in p.rglob('*') if f.is_file()))

    def test_idempotent(self):
        self.run_install()
        count = len(self.calls)
        r = self.run_install()
        self.assertEqual(r['status'], 'already_installed')
        self.assertEqual(len(self.calls), count)

    def test_local_credentials_preserved(self):
        self.run_install()
        p = self.home / 'profiles/minora-ai-search-us/.env'
        p.write_text('OWN_KEY=private')
        self.run_install()
        self.assertEqual(p.read_text(), 'OWN_KEY=private')

    def test_existing_unmanaged_profile_refused(self):
        p = self.home / 'profiles/minora-ai-search-us'
        p.mkdir(parents=True)
        (p / 'SOUL.md').write_text('Another profile')
        with self.assertRaises(ValueError):
            self.run_install()
        self.assertEqual((p / 'SOUL.md').read_text(), 'Another profile')

    def test_changed_skill_refused(self):
        self.run_install()
        p = self.home / 'profiles/minora-ai-search-us/skills/minora-test-0/SKILL.md'
        p.write_text('Local edit')
        with self.assertRaises(ValueError):
            self.run_install()
        self.assertEqual(p.read_text(), 'Local edit')

    def test_corrupt_bundle_refused_before_cli(self):
        (self.bundle / 'skills/minora-test-0/SKILL.md').write_text('tampered')
        with self.assertRaises(ValueError):
            self.run_install()
        self.assertEqual(self.calls, [])

    def test_manifest_path_escape(self):
        p = self.bundle / 'manifest.json'
        m = json.loads(p.read_text())
        m['files']['../escape'] = '0' * 64
        p.write_text(json.dumps(m))
        with self.assertRaises(ValueError):
            self.run_install()

    def test_symlink_bundle_refused(self):
        p = self.bundle / 'skills/minora-test-0/SKILL.md'
        raw = p.read_text()
        p.unlink()
        other = self.root / 'other'
        other.write_text(raw)
        p.symlink_to(other)
        with self.assertRaises(ValueError):
            self.run_install()

    def test_unlisted_payload_file_refused(self):
        (self.bundle / 'skills/minora-test-0/rogue.py').write_text('pass')
        with self.assertRaises(ValueError):
            self.run_install()

    def test_manifest_cannot_change_profile(self):
        p = self.bundle / 'manifest.json'
        m = json.loads(p.read_text())
        m['name'] = 'default'
        p.write_text(json.dumps(m))
        with self.assertRaises(ValueError):
            self.run_install()

    def test_secret_manifest_entry_refused(self):
        p = self.bundle / 'manifest.json'
        m = json.loads(p.read_text())
        m['files']['.env'] = hashlib.sha256(b'x').hexdigest()
        (self.bundle / '.env').write_text('x')
        p.write_text(json.dumps(m))
        with self.assertRaises(ValueError):
            self.run_install()

    def test_failed_cli_not_success(self):
        def fail(args, env):
            if args == ['profile', 'install', '--help']:
                return 0, '--name --yes'
            if args == ['--version']:
                return 0, '0.19.0'
            return 1, 'private_key=never-log-this'
        with self.assertRaises(ValueError) as err:
            module.install(self.bundle, self.home, apply=True, runner=fail)
        self.assertNotIn('never-log-this', str(err.exception))

    def test_unsupported_cli_refused(self):
        with self.assertRaises(ValueError):
            module.install(self.bundle, self.home, apply=True, runner=lambda a, e: (2, 'unknown command'))

    def test_no_gateway_or_model_calls(self):
        self.run_install()
        text = repr(self.calls)
        for forbidden in ['gateway', '--force', 'chat', '--clone', 'profile use']:
            self.assertNotIn(forbidden, text)

    def test_readback_missing_file_fails(self):
        original = self.cli
        def broken(args, env):
            r = original(args, env)
            if args[:2] == ['profile', 'install'] and '--help' not in args:
                (self.home / 'profiles/minora-ai-search-us/skills/minora-test-1/SKILL.md').unlink()
            return r
        with self.assertRaises(ValueError):
            module.install(self.bundle, self.home, apply=True, runner=broken)

    def test_profile_is_not_sandbox_claim(self):
        r = self.run_install()
        self.assertFalse(r['nick_access_ready'])

    def test_empty_manifest_path_rejected_cleanly(self):
        p = self.bundle / 'manifest.json'
        m = json.loads(p.read_text())
        m['files'][''] = '0' * 64
        p.write_text(json.dumps(m))
        with self.assertRaises(ValueError):
            self.run_install()

    def test_staging_parent_symlink_refused(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (self.home / 'minora-distributions').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.run_install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_added_mcp_is_config_drift(self):
        self.run_install()
        p = self.home / 'profiles/minora-ai-search-us/config.yaml'
        c = json.loads(p.read_text())
        c['mcp_servers'] = {'unexpected': {'command': 'danger'}}
        p.write_text(json.dumps(c))
        with self.assertRaises(ValueError):
            self.run_install()

    def test_receipt_cannot_hide_payload_changes(self):
        self.run_install()
        base = self.home / 'profiles/minora-ai-search-us'
        f = base / 'skills/minora-test-0/SKILL.md'
        f.write_text('Local modification')
        rp = base / '.minora-install.json'
        receipt = json.loads(rp.read_text())
        receipt['installed_files']['skills/minora-test-0/SKILL.md'] = hashlib.sha256(f.read_bytes()).hexdigest()
        rp.write_text(json.dumps(receipt))
        with self.assertRaises(ValueError):
            self.run_install()

    def test_root_profile_mutation_is_detected(self):
        original = self.cli
        def bad_native(args, env):
            result = original(args, env)
            if args[:2] == ['profile', 'install'] and '--help' not in args:
                (self.home / '.env').write_text('unexpected change')
            return result
        with self.assertRaises(ValueError):
            module.install(self.bundle, self.home, apply=True, runner=bad_native)

    def test_non_object_manifest_rejected(self):
        (self.bundle / 'manifest.json').write_text('[]')
        with self.assertRaises(ValueError):
            self.run_install()

    def test_nested_unexpected_skill_refused(self):
        self.run_install()
        p = self.home / 'profiles/minora-ai-search-us/skills/category/unexpected/SKILL.md'
        p.parent.mkdir(parents=True)
        p.write_text('Extra skill')
        with self.assertRaises(ValueError):
            self.run_install()

    def test_native_cannot_silently_copy_root_credentials(self):
        original = self.cli
        def bad_native(args, env):
            result = original(args, env)
            if args[:2] == ['profile', 'install'] and '--help' not in args:
                source = self.home / '.env'
                dest = self.home / 'profiles/minora-ai-search-us/.env'
                shutil.copyfile(source, dest)
            return result
        with self.assertRaises(ValueError):
            module.install(self.bundle, self.home, apply=True, runner=bad_native)


if __name__ == '__main__':
    unittest.main()
