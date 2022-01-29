import nox
from pathlib import Path
import re


nox.options.sessions = []

VERS = re.compile(
    r"""\
^- repo: (.*?)
  rev: (.*?)$""",
    re.MULTILINE,
)

REPL_LINE = '''\
- repo: {0}
  rev: "{1}"'''


@nox.session(reuse_venv=True)
def bump(session: nox.Session) -> None:
    session.install("lastversion")

    style = Path("pages/developers/style.md")
    txt = style.read_text()
    old_versions = {m[1]: m[2].strip('"') for m in VERS.finditer(txt)}

    for proj, old_version in old_versions.items():
        new_version = session.run("lastversion", proj, silent=True).strip()

        if old_version.lstrip("v") == new_version:
            continue

        if old_version.startswith("v"):
            new_version = f"v{new_version}"

        before = REPL_LINE.format(proj, old_version)
        after = REPL_LINE.format(proj, new_version)

        session.log(f"Bump: {old_version} -> {new_version}")
        txt = txt.replace(before, after)

    style.write_text(txt)
