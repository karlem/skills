import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location('library_' + name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LibraryChecks(unittest.TestCase):
    def test_library_validation(self):
        errors, counts = load('validate').validate()
        self.assertEqual(errors, [])
        self.assertEqual(counts['skills'], 11)

    def test_installer_preserves_existing_skill(self):
        module = load('install')
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'skills'
            dest.mkdir()
            existing = dest / 'distributed-systems'
            existing.mkdir()
            (existing / 'user-content').write_text('keep')
            with self.assertRaises(FileExistsError):
                module.install(dest, ['linux-performance', 'distributed-systems'])
            self.assertEqual((existing / 'user-content').read_text(), 'keep')
            self.assertFalse((dest / 'linux-performance').exists())

    def test_installer_rejects_unknown_and_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('missing', '../distributed-systems'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    load('install').install(tmp, [name])

    def test_installer_refuses_checkout_destination(self):
        with self.assertRaises(ValueError):
            load('install').install(ROOT / '.agents/skills', ['distributed-systems'])

    def test_installer_dry_run_has_no_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'absent'
            load('install').install(dest, ['distributed-systems'], dry_run=True)
            self.assertFalse(dest.exists())

    def test_installed_skills_are_self_contained(self):
        index = json.loads((ROOT / 'sources/skills-index.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'skills'
            load('install').install(dest, [x['name'] for x in index])
            for item in index:
                path = dest / item['name']
                self.assertTrue((path / 'SKILL.md').is_file())
                for source in (ROOT / item['path']).rglob('*'):
                    if source.is_file():
                        self.assertEqual(source.read_bytes(), (path / source.relative_to(ROOT / item['path'])).read_bytes())
            self.assertEqual(len(list(dest.iterdir())), len(index))

    def test_pptx_numeric_slide_order(self):
        module = load('research')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'synthetic.pptx'
            with zipfile.ZipFile(path, 'w') as archive:
                for number in (10, 2, 1):
                    archive.writestr(f'ppt/slides/slide{number}.xml', f'<a:root xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:t>text-{number}</a:t></a:root>')
            text = module.pptx_text(path)
            self.assertLess(text.index('text-1\n'), text.index('text-2\n'))
            self.assertLess(text.index('text-2\n'), text.index('text-10'))

    def test_html_cleanup_discards_script_and_navigation(self):
        try:
            import bs4  # noqa: F401
        except ImportError:
            self.skipTest('Optional research HTML dependency unavailable')
        module = load('research')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'synthetic.html'
            path.write_text('<html><nav>menu</nav><script>runSomething()</script><main><h1>Heading</h1><p>Technical mechanism.</p></main></html>')
            self.assertEqual(module.html_text(path), 'Heading\nTechnical mechanism.')


if __name__ == '__main__':
    unittest.main()
