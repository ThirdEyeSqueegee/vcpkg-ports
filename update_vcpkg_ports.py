from hashlib import sha512
from json import dump, load
from re import sub
from subprocess import run
from urllib.request import urlretrieve

spdlog_repo = "https://github.com/gabime/spdlog"

spdlog_ref, spdlog_tag = (
    run(
        ["git", "ls-remote", "--tags", "--sort=-v:refname", spdlog_repo],
        capture_output=True,
    )
    .stdout.decode()
    .splitlines()[0]
    .split()
)

spdlog_tag = spdlog_tag.replace("refs/tags/v", "")

# Update baseline.json
with open("./versions/baseline.json", "r") as f:
    baseline = load(f)

baseline["default"]["spdlog"]["baseline"] = spdlog_tag

with open("./versions/baseline.json", "w") as f:
    dump(baseline, f, indent=2)

# Update spdlog/vcpkg.json
with open("./ports/spdlog/vcpkg.json", "r") as f:
    vcpkg_json = load(f)

vcpkg_json["version-semver"] = spdlog_tag

with open("./ports/spdlog/vcpkg.json", "w") as f:
    dump(vcpkg_json, f, indent=2)

# Update versions/s-/spdlog.json
with open("./versions/s-/spdlog.json", "r") as f:
    spdlog_json = load(f)

spdlog_json["versions"][0]["version-semver"] = spdlog_tag

with open("./versions/s-/spdlog.json", "w") as f:
    dump(spdlog_json, f, indent=2)

# Update spdlog portfile
spdlog_archive, _ = urlretrieve(f"{spdlog_repo}/archive/refs/tags/v{spdlog_tag}.tar.gz")

with open(spdlog_archive, "rb") as f:
    spdlog_sha = sha512(f.read()).hexdigest()

with open("./ports/spdlog/portfile.cmake", "r") as f:
    portfile = f.readlines()
    portfile[3] = sub(r"(REF).*", f"REF v{spdlog_tag}", portfile[3])
    portfile[4] = sub(r"(SHA512).*", f"SHA512 {spdlog_sha}", portfile[4])

with open("./ports/spdlog/portfile.cmake", "w") as f:
    f.writelines(portfile)