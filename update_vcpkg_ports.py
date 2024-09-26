from hashlib import sha512
from json import dumps, load
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
with open("./versions/baseline.json") as f:
    baseline = load(f)

baseline["default"]["spdlog"]["baseline"] = spdlog_tag

baseline_str = dumps(baseline, indent=2)
baseline_str += "\r\n"

with open("./versions/baseline.json", "w", newline="\r\n") as f:
    f.write(baseline_str)

# Update spdlog/vcpkg.json
with open("./ports/spdlog/vcpkg.json") as f:
    vcpkg_json = load(f)

vcpkg_json["version-semver"] = spdlog_tag

vcpkg_json_str = dumps(vcpkg_json, indent=2)
vcpkg_json_str += "\r\n"

with open("./ports/spdlog/vcpkg.json", "w", newline="\r\n") as f:
    f.write(vcpkg_json_str)

# Update versions/s-/spdlog.json
with open("./versions/s-/spdlog.json") as f:
    spdlog_json = load(f)

spdlog_json["versions"][0]["version-semver"] = spdlog_tag

spdlog_json_str = dumps(spdlog_json, indent=2)
spdlog_json_str += "\r\n"

with open("./versions/s-/spdlog.json", "w", newline="\r\n") as f:
    f.write(spdlog_json_str)

# Update spdlog portfile
spdlog_archive, _ = urlretrieve(f"{spdlog_repo}/archive/refs/tags/v{spdlog_tag}.tar.gz")

with open(spdlog_archive, "rb") as f:
    spdlog_sha = sha512(f.read()).hexdigest()

with open("./ports/spdlog/portfile.cmake") as f:
    portfile = f.readlines()

portfile[3] = sub(r"(REF).*", f"REF v{spdlog_tag}", portfile[3])
portfile[4] = sub(r"(SHA512).*", f"SHA512 {spdlog_sha}", portfile[4])

with open("./ports/spdlog/portfile.cmake", "w", newline="\r\n") as f:
    f.writelines(portfile)
