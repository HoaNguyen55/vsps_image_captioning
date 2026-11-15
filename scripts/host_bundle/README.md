# Host install bundle (system packages for rented hosts)

Every rented machine is a freshly rented one (PI-1115r). Its image can lack any system library, even one that an
earlier image of the same offer had. On 2026-11-15 the hD image lacked seven base libraries (libfontconfig1,
libfreetype6, libglib2.0-0t64, libharfbuzz0b, libpng16-16t64, libjpeg-turbo8, libxml2), plus liblcms2-2, libnss3 and
libnspr4. The PDF tool setup then stopped with rc 9 at its `ldd` check, and three of the four jobs were dropped
(`.session_backup/2026-11-15/host_session_hD/setup/rec/missing_libs.txt`).

This bundle makes the system side of a host the same every time:

| File | What it is |
|---|---|
| `SYSTEM_PACKAGES.txt` | One Ubuntu 24.04 package per line, with its profile and the job or evidence that needs it |
| `cleanup_host.sh` | Laptop clean-up after the host is deleted (section "After the host is deleted") |
| `install_system.sh` | One `apt-get update` and one `apt-get install -y --no-install-recommends --no-upgrade` of the chosen profiles (a package that is already installed is not upgraded), then a verification table |

Profiles: `base` (every job: git, tmux, rsync, flock, curl, python3.12 with venv), `figures` (nothing beyond base:
the matplotlib and pillow wheels carry their own libraries; K1 built on the hD image with base only), `pdf` (the
libraries and fonts the private rsvg-convert, poppler tools and TinyTeX link against), `gpu` (C compiler and
Python headers for torch inductor), `java` (optional, only by name: VnCoreNLP, METEOR, SPICE). `all` = base,
figures, pdf and gpu. The private PDF tools themselves (the DEBS list of `host_tex_setup.sh`) stay private; this
bundle installs only what they link against.

## On a fresh host: the first step after access, before any job

1. After the Access and Facts steps of the skill (`.claude/skills/running-rented-gpu-jobs/SKILL.md`, steps 2-3),
   push this folder with the code and run, as root:

   ```bash
   bash scripts/host_bundle/install_system.sh <profiles of this session's jobs>   # e.g. pdf gpu
   ```

   The script waits up to 10 minutes for the dpkg lock (fresh images often run unattended-upgrades after boot).
2. Read the table. `VERIFY CLEAN` (rc 0) is the only state in which a job may start. `VERIFY FAILED` (rc 1)
   names every missing item in its `MISSING` lines; fix them (install the package the line names, or add a missing
   package to the list as below) and run the same command again. A missing GPU driver (`nvidia-smi` row) is not
   installable here: it is a FAULT of the host under the skill's Facts step.
3. Put the table, with dots written as underscores, into the session's facts-and-packages OPS line.
4. Run every apt call before the first job or tool setup starts. The run docs forbid apt calls after their setup
   step; a later install happens only where the run doc's stop rule allows it.

`--verify <profiles>` repeats the checks without installing. The pdf rows check the sonames in the `ldconfig`
cache before the private tools exist, and the private tools under `/root/paperC_build` with `ldd` once they do
(`BUNDLE_BUILD_DIR` changes that folder). The font row checks that the system fontconfig resolves "DejaVu Sans" and "DejaVu Serif" (the mainfont of the Paper B build)
(`BUNDLE_FONTS`, a comma-separated list, changes them).

**The rule: a job never starts before the verification table is clean for the profiles it needs.**

## After every session: refresh the list

1. Read the session's records for anything missing: setup logs with `not found`, `STOP` lines that name a library,
   `dpkg -s` output, and any package installed by hand on the host.
2. Add each missing package to `SYSTEM_PACKAGES.txt` in its group, with its profile and a comment that names the job,
   the date and the evidence file, in the form already used there, for example:
   `libfoo1  pdf  # rsvg-convert: libfoo.so.1 not found (2026-11-20, host_session_hX/setup/rec/setup_out.txt)`.
3. Run `bash scripts/host_bundle/install_system.sh --selftest` on the laptop (it installs nothing; it checks the list
   parses and that apt knows every name). The new list sha goes into the next run doc.
4. If a package name is wrong for 24.04 (the selftest's `apt knows` line fails), find the right one with
   `apt-cache search` or `dpkg -S <library file>` on a 24.04 machine before the next rental.

## After the host is deleted: clean-up (PI-1115s)

Once the machine is deleted on the panel and L-after is done (also after a lost host), every laptop file about
that machine is removed, except logs. This is the last step of the session:

```bash
bash scripts/host_bundle/cleanup_host.sh <alias> --dry-run   # lists only
bash scripts/host_bundle/cleanup_host.sh <alias>             # removes, then prints the OPS text
```

| Removed | Kept |
|---|---|
| the alias's `Host` block in `~/.ssh/config` (the script stops if that `Host` line names other aliases too) | LOG lines |
| its host keys (`ssh-keygen -R` for the alias, the address, the `[address]:port` form, any HostKeyAlias) and the `.old` copy that `ssh-keygen -R` leaves | the session record folder under `.session_backup/` (logs, sums, pulled results) |
| a per-host known_hosts file, only when its name carries the alias (`~/.ssh/known_hosts_<alias>`); any other UserKnownHostsFile loses this host's keys and keeps its other entries | `*.log` files, and anything inside a git work tree |
| its control socket | pid files of processes that are still alive (stop them first by the skill's rule) |
| askpass scripts, password files and pid files whose name carries the alias, in `~/.config/vsps`, `~` and `/tmp` (depth 1) | |

The last line it prints is the text of the clean-up OPS line: names only, never an address. Write it to the LOG
as one OPS line.

## What the laptop could not check

The list was built from the hD records and from `ldd` of the same tool builds on the laptop (Ubuntu 24.04.1). The
laptop already has these libraries, so the full install on a minimal image, the order of apt's resolution there and
the result of the font check on a host image are first seen on the next fresh host.
