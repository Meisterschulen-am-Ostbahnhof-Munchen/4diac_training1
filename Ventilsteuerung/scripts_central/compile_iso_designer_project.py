r"""Compile an ISO-Designer project via the CLI /Compile flag instead of
building manually in the IDE.

Undocumented flag confirmed by Bucher Automation Support (2026-09-23):
    ISODesigner.exe /Compile <project>.jvp
writes Output/CompileLog.txt with the build result, but does not terminate
the process afterwards (even on success, with no window ever shown) - this
script starts it, polls for the log file, then kills only that one process
(by PID/handle, never by image name) so any other, genuinely open
ISO-Designer GUI session on the same machine is left untouched.

No path is hardcoded - the pool directory is always a required argument (see
--pool-dir below), matching GcfScript.py's/list_mask_objects.py's convention
in this same folder. Project-specific invocation goes through a thin .bat
wrapper (which supplies the concrete relative path for that project) plus an
IDE .launch entry, not by editing this file.

IMPORTANT: the ISODesigner.exe subprocess's own current working directory at
launch affects some relative paths it writes back into the project's own
<Project>.jpuo (user-options) file, e.g. the Deployment path - confirmed by
an accidental corruption during development (an unrelated caller cwd turned
a short ".\Deployment\" into a long, wrong "..\..\...\" chain). This script
always launches ISODesigner.exe with cwd=<pool_dir> to avoid that.

Usage:
    python compile_iso_designer_project.py --pool-dir <path/to/DefaultPool>
    python compile_iso_designer_project.py --pool-dir <path> --jvp Other.jvp
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

ISODESIGNER_EXE = (
    r"C:\Program Files (x86)\Bucher Automation\ISODesigner 5.7.2"
    r"\ISO-Designer\Bin\ISODesigner.exe"
)
# ISODesigner writes this line (with varying Warnings/Errors counts) exactly
# once, as the LAST line, when the build truly finishes - success or not.
# Polling for it (not just for the log file's existence) is required: on
# slower/image-heavy pools the log file is created early and still being
# written to when a fixed short sleep would already kill the process,
# truncating the output and reporting a false failure (confirmed review
# finding on training1 PR #268).
BUILD_FINISHED_MARKER = "Build finished."
SUCCESS_MARKER = "Build finished. 0 Warnings, 0 Errors"
POLL_TIMEOUT_S = 90
REPO_ROOT_PLACEHOLDER = "<REPO_ROOT>"


def parse_args():
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-d", "--pool-dir", dest="pool_dir", required=True,
        help="ISO-Designer pool workspace folder (the one containing the "
             ".jvp file), relative to this script's parent directory "
             "(i.e. relative to the project's Ventilsteuerung/ folder) - "
             "e.g. ISO-DesignerProjects/Workspace_AI/DefaultPool",
    )
    parser.add_argument(
        "-j", "--jvp", dest="jvp_file", default="DefaultPool.jvp",
        help="Project file name inside --pool-dir (default: DefaultPool.jvp)",
    )
    args = parser.parse_args()
    pool_dir = (script_dir.parent / args.pool_dir).resolve()
    return pool_dir, pool_dir / args.jvp_file, script_dir.parent.parent


def main() -> int:
    pool_dir, jvp_path, repo_root = parse_args()

    if not Path(ISODESIGNER_EXE).exists():
        print(f"ISODesigner.exe nicht gefunden: {ISODESIGNER_EXE}")
        return 1
    if not jvp_path.exists():
        print(f"Projektdatei nicht gefunden: {jvp_path}")
        return 1

    compile_log = pool_dir / "Output" / "CompileLog.txt"
    compile_log.unlink(missing_ok=True)

    # cwd MUST be the project's own directory - see module docstring.
    proc = subprocess.Popen([ISODESIGNER_EXE, "/Compile", str(jvp_path)], cwd=pool_dir)
    try:
        deadline = time.monotonic() + POLL_TIMEOUT_S
        log_text = ""
        while time.monotonic() < deadline:
            if compile_log.exists():
                log_text = compile_log.read_text(encoding="utf-8", errors="replace")
                if BUILD_FINISHED_MARKER in log_text:
                    break
            time.sleep(1)
        else:
            if compile_log.exists():
                print(f"Timeout - CompileLog.txt erschienen, aber nie mit '{BUILD_FINISHED_MARKER}' "
                      f"abgeschlossen (Build haengt vermutlich fest) - siehe {compile_log}.")
            else:
                print("Timeout - CompileLog.txt nie erschienen (ISODesigner haengt vermutlich an einem Dialog fest).")
            return 1
        time.sleep(1)  # let it finish flushing/closing the file after the terminal line
        log_text = compile_log.read_text(encoding="utf-8", errors="replace")
    finally:
        # Kill only the process we started (by PID) - never touches an
        # unrelated, genuinely open ISO-Designer GUI session.
        proc.kill()
        proc.wait(timeout=10)

    # ISODesigner embeds the caller's absolute checkout path in the log (e.g.
    # in the "Compiling ISO objectpool ... <path>\Output\DefaultPool.iop"
    # line) - normalize it before committing, so a rebuild from a different
    # checkout location doesn't produce machine-specific source-control churn.
    normalized_text = log_text.replace(str(repo_root), REPO_ROOT_PLACEHOLDER)
    if normalized_text != log_text:
        compile_log.write_text(normalized_text, encoding="utf-8")
    log_text = normalized_text

    print(log_text)
    if SUCCESS_MARKER not in log_text:
        print(f"Build FEHLGESCHLAGEN (kein '{SUCCESS_MARKER}' im Log) - siehe {compile_log}")
        return 1

    print("Build erfolgreich.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
