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

    new_versions = {
        proj: session.run("lastversion", proj, "--pre", silent=True).strip()
        for proj in old_versions
    }

    changed_versions = {
        proj: new_versions[proj]
        for proj in old_versions
        if old_versions[proj].lstrip("v") != new_versions[proj]
    }

    for proj, vers in changed_versions.items():
        if old_versions[proj].startswith("v"):
            vers = f"v{vers}"
        before = REPL_LINE.format(proj, old_versions[proj])
        after = REPL_LINE.format(proj, vers)
        session.log(f"Bump: {old_versions[proj]} -> {vers}")
        txt = txt.replace(before, after)

    style.write_text(txt)
