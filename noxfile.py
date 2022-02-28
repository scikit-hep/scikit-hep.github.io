from pathlib import Path
import json
import nox
import re
import urllib.request


nox.options.sessions = []

PC_VERS = re.compile(
    r"""\
^- repo: (.*?)
  rev: (.*?)$""",
    re.MULTILINE,
)

PC_REPL_LINE = '''\
- repo: {0}
  rev: "{1}"'''


GHA_VERS = re.compile(r"[\s\-]+uses: (.*?)@([^\s]+)")

@nox.session(reuse_venv=True)
def pc_bump(session: nox.Session) -> None:
    session.install("lastversion")

    style = Path("pages/developers/style.md")
    txt = style.read_text()
    old_versions = {m[1]: m[2].strip('"') for m in PC_VERS.finditer(txt)}

    for proj, old_version in old_versions.items():
        new_version = session.run("lastversion", proj, silent=True).strip()

        if old_version.lstrip("v") == new_version:
            continue

        if old_version.startswith("v"):
            new_version = f"v{new_version}"

        before = PC_REPL_LINE.format(proj, old_version)
        after = PC_REPL_LINE.format(proj, new_version)

        session.log(f"Bump: {old_version} -> {new_version}")
        txt = txt.replace(before, after)

    style.write_text(txt)


@nox.session(venv_backend="none")
def gha_bump(session: nox.Session) -> None:

    pages = list(Path("pages/developers").glob("gha_*.md"))
    full_txt = "\n".join(page.read_text() for page in pages)

    # This assumes there is a single version per action
    old_versions = {m[1]: m[2] for m in GHA_VERS.finditer(full_txt)}

    for repo, old_version in old_versions.items():
        response = urllib.request.urlopen(f"https://api.github.com/repos/{repo}/tags")
        tags_js = json.loads(response.read())
        tags = [x["name"] for x in tags_js if x["name"].count(".") == old_version.count(".")]
        new_version = tags[0]
        if new_version != old_version:
            print(f"Convert {repo}: {old_version} -> {new_version}")
            for page in pages:
                txt = page.read_text()
                txt.replace(f"uses: {repo}@{old_version}", f"uses: {repo}@{new_version}")
                page.write_text(txt)
