from json import dump, load
from subprocess import run

# Update spdlog git-tree
spdlog_git_tree = run(
    ["git", "rev-parse", "HEAD:ports/spdlog"], capture_output=True
).stdout.decode()

with open("./versions/s-/spdlog.json", "r") as f:
    version = load(f)

version["versions"][0]["git-tree"] = spdlog_git_tree.strip("\n")

with open("./versions/s-/spdlog.json", "w") as f:
    dump(version, f, indent=2)
