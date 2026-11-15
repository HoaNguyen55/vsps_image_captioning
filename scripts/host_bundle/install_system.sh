#!/bin/bash
# Install and verify the system packages of a fresh Ubuntu 24.04 rented host, before any job (PI-1115r).
#   bash install_system.sh <profile>...            as root: apt-get update, one apt-get install, then the checks
#   bash install_system.sh --verify <profile>...   the checks only; installs nothing
#   bash install_system.sh --selftest              parsing and package-name checks on this machine; installs nothing
# Profiles: base figures pdf gpu java all (all = base figures pdf gpu; java only by name; base is always included).
# The package list is SYSTEM_PACKAGES.txt beside this script. Exit: 0 = verification clean, 1 = something missing
# (named in the last lines), 2 = usage or list error. Re-running is safe: installed packages are left as they are.
set -u -o pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
LIST=${BUNDLE_LIST:-$HERE/SYSTEM_PACKAGES.txt}
FONTS=${BUNDLE_FONTS:-DejaVu Sans,DejaVu Serif}   # comma-separated; DejaVu Serif is the mainfont of the Paper B build (K5)
B=${BUNDLE_BUILD_DIR:-/root/paperC_build}   # private PDF tool tree of the run docs; checked only where it exists
PATH=$PATH:/usr/sbin:/sbin                    # ldconfig
KNOWN=" base figures pdf gpu java "
# sonames the private PDF tools need from the system: the "not found" lines of the 15 Nov hD setup
# (host_session_hD/setup/rec/missing_libs.txt) plus the laptop ldd of the same tool builds
SONAMES="libfontconfig.so.1 libfreetype.so.6 libglib-2.0.so.0 libgio-2.0.so.0 libgobject-2.0.so.0
libgmodule-2.0.so.0 libharfbuzz.so.0 libpng16.so.16 libjpeg.so.8 libxml2.so.2 liblcms2.so.2 libnss3.so
libnssutil3.so libsmime3.so libnspr4.so libplc4.so libplds4.so libcurl-gnutls.so.4 libgraphite2.so.3 libexpat.so.1"

profiles() {  # profiles <arg>...: the sorted profile set, base always in it
  local p out=base
  for p in "$@"; do
    case $p in
      all) out="$out figures pdf gpu" ;;
      base | figures | pdf | gpu | java) out="$out $p" ;;
      *) echo "unknown profile: $p (base figures pdf gpu java all)" >&2; return 2 ;;
    esac
  done
  printf '%s\n' $out | sort -u | tr '\n' ' ' | sed 's/ $//'
}

packages() {  # packages "<profile set>": package names tagged with any profile of the set, in file order
  awk -v want=" $1 " -v known="$KNOWN" '
    { sub(/#.*/, "") }
    NF == 0 { next }
    NF != 2 { printf "list line %d: want <package> <profiles>, got %d fields\n", NR, NF > "/dev/stderr"; bad = 1; next }
    dup[$1]++ { printf "list line %d: %s listed twice\n", NR, $1 > "/dev/stderr"; bad = 1; next }
    { n = split($2, t, ",")
      for (i = 1; i <= n; i++) {
        if (!index(known, " " t[i] " ")) { printf "list line %d: unknown profile %s\n", NR, t[i] > "/dev/stderr"; bad = 1 }
        else if (index(want, " " t[i] " ") && !seen[$1]++) print $1
      } }
    END { exit bad ? 2 : 0 }' "$LIST"
}

FAILED=()
row() {  # row <check> <item> <status>; a status not starting with ok/skip is a failure
  printf '%-7s %-40s %s\n' "$1" "$2" "$3"
  case $3 in ok* | skip*) ;; *) FAILED+=("$1 $2: $3") ;; esac
}

ldd_row() {  # ldd_row <label> <binary> [LD_LIBRARY_PATH]
  local miss
  miss=$(LD_LIBRARY_PATH=${3:-} ldd "$(readlink -f "$2")" 2>&1 | awk '/not found/ {print $1}' | tr '\n' ' ')
  if [ -n "$miss" ]; then row ldd "$1" "not found: $miss"; else row ldd "$1" ok; fi
}

verify() {  # verify "<profile set>"
  local set=" $1 " p t s v tmp
  FAILED=()
  printf '%-7s %-40s %s\n' CHECK ITEM STATUS
  for p in $(packages "$1"); do
    if [ "$(dpkg-query -W -f='${Status}' "$p" 2> /dev/null)" = "install ok installed" ]; then
      row dpkg "$p" "ok $(dpkg-query -W -f='${Version}' "$p")"
    else row dpkg "$p" "not installed"; fi
  done
  local tools="git tmux rsync flock setsid curl wget xz tar sha256sum pgrep python3.12"
  case $set in *" pdf "*) tools="$tools perl fc-match fc-list" ;; esac
  case $set in *" gpu "*) tools="$tools gcc g++ make" ;; esac
  case $set in *" java "*) tools="$tools java" ;; esac
  for t in $tools; do
    if command -v "$t" > /dev/null; then ldd_row "$t" "$(command -v "$t")"; else row tool "$t" "not on PATH"; fi
  done
  case $set in *" pdf "*)
    local have
    have=" $(ldconfig -p | awk 'NR > 1 {print $1}' | sort -u | tr '\n' ' ') "
    for s in $SONAMES; do
      case $have in *" $s "*) row soname "$s" ok ;; *) row soname "$s" "not in the ldconfig cache" ;; esac
    done
    for t in rsvg-convert pdfinfo pdftotext pdffonts; do
      if [ -x "$B/prefix/usr/bin/$t" ]; then ldd_row "private $t" "$B/prefix/usr/bin/$t" "$B/prefix/usr/lib/x86_64-linux-gnu"
      else row ldd "private $t" "skip (no $B/prefix yet)"; fi
    done
    for t in luahbtex pdftex xetex bibtex kpsewhich; do
      if [ -x "$B/TinyTeX/bin/x86_64-linux/$t" ]; then ldd_row "TinyTeX $t" "$B/TinyTeX/bin/x86_64-linux/$t"
      else row ldd "TinyTeX $t" "skip (no $B/TinyTeX yet)"; fi
    done
    local font
    while IFS= read -r font; do
      v=$(env -u FONTCONFIG_FILE fc-match -f '%{family}' "$font" 2> /dev/null)
      case ",$v," in *",$font,"*) row font "$font" "ok ($(env -u FONTCONFIG_FILE fc-match -f '%{file}' "$font"))" ;;
                     *) row font "$font" "fc-match gives '${v:-nothing}'" ;; esac
    done < <(tr ',' '\n' <<< "$FONTS") ;;
  esac
  v=$(python3.12 -V 2>&1)
  case $v in "Python 3.12."*) row python python3.12 "ok $v" ;; *) row python python3.12 "${v:-absent}" ;; esac
  tmp=$(mktemp -d)
  if python3.12 -m venv "$tmp/v" > "$tmp/log" 2>&1 && "$tmp/v/bin/python" -m pip --version > /dev/null 2>&1; then
    row python "venv with pip" ok
  else row python "venv with pip" "fails: $(tail -n 1 "$tmp/log")"; fi
  rm -rf "$tmp"
  case $set in *" gpu "*)
    if [ -f /usr/include/python3.12/Python.h ]; then row python Python.h ok; else row python Python.h absent; fi
    if nvidia-smi -L > /dev/null 2>&1; then row gpu nvidia-smi "ok $(nvidia-smi -L | head -n 1 | cut -c1-40)"
    else row gpu nvidia-smi "fails: the driver belongs to the host image, not this bundle (skill step 3: FAULT)"; fi ;;
  esac
  if pgrep -x apt-get > /dev/null || pgrep -x dpkg > /dev/null; then row apt idle "apt-get or dpkg still running"
  else row apt idle ok; fi
  echo
  if [ ${#FAILED[@]} = 0 ]; then echo "VERIFY CLEAN (profiles: $1)"; return 0; fi
  echo "VERIFY FAILED (profiles: $1): ${#FAILED[@]} item(s) missing; no job may start"
  printf '  MISSING %s\n' "${FAILED[@]}"
  return 1
}

do_install() {  # do_install "<profile set>"
  local pk
  [ "$(id -u)" = 0 ] || { echo "install needs root (or use --verify)"; return 2; }
  pk=$(packages "$1") || return 2
  export DEBIAN_FRONTEND=noninteractive
  # a fresh image often runs unattended-upgrades right after boot: wait for the dpkg lock instead of failing
  apt-get -o DPkg::Lock::Timeout=600 update || echo "apt-get update failed (rc $?); the checks below say what is missing"
  # shellcheck disable=SC2086
  apt-get -o DPkg::Lock::Timeout=600 install -y --no-install-recommends --no-upgrade $pk \
    || echo "apt-get install failed (rc $?); the checks below say what is missing"
}

selftest() {
  local n=0 bad=0 p set fx out rc
  ok() { n=$((n + 1)); if eval "$2"; then echo "ok   $1"; else echo "FAIL $1"; bad=$((bad + 1)); fi; }
  ok "profiles all = base figures gpu pdf" '[ "$(profiles all)" = "base figures gpu pdf" ]'
  ok "profiles java = base java" '[ "$(profiles java)" = "base java" ]'
  ok "profiles pdf pdf base = base pdf" '[ "$(profiles pdf pdf base)" = "base pdf" ]'
  ok "unknown profile is rc 2" '[ "$(profiles pdfx 2> /dev/null; echo $?)" = 2 ]'
  ok "the list parses with rc 0" 'packages "base figures pdf gpu java" > /dev/null'
  for set in base "base figures" "base pdf" "base gpu" "base java"; do
    ok "profile set '$set' is not empty" '[ -n "$(packages "$set")" ]'
  done
  ok "figures adds nothing to base (K1 evidence)" '[ "$(packages "base figures")" = "$(packages base)" ]'
  ok "base is inside every profile" '[ -z "$(comm -23 <(packages base | sort) <(packages "base pdf" | sort))" ]'
  ok "java is not in all" '! packages "$(profiles all)" | grep -qx default-jre-headless'
  for p in libfontconfig1 libfreetype6 libglib2.0-0t64 libharfbuzz0b libpng16-16t64 libjpeg-turbo8 libxml2 \
           liblcms2-2 libnss3 libnspr4 fontconfig fonts-dejavu-core; do
    ok "pdf has $p" 'packages "base pdf" | grep -qx "$p"'
  done
  fx=$(mktemp)
  printf 'a base\nb base extra\n' > "$fx"; ok "a 3-field line is rc 2" '[ "$(LIST=$fx packages base 2> /dev/null > /dev/null; echo $?)" = 2 ]'
  printf 'a base\na pdf\n' > "$fx"; ok "a duplicate package is rc 2" '! LIST=$fx packages base 2> /dev/null > /dev/null'
  printf 'a basse\n' > "$fx"; ok "an unknown tag is rc 2" '! LIST=$fx packages base 2> /dev/null > /dev/null'
  printf 'a base,pdf  # c\n# x y z\nb pdf\n' > "$fx"; ok "comments and tag lists parse" '[ "$(LIST=$fx packages "base pdf" | tr "\n" " ")" = "a b " ]'
  rm -f "$fx"
  ok "row: ok and skip pass, anything else fails" 'FAILED=(); row x a ok > /dev/null; row x b "skip (y)" > /dev/null; row x c absent > /dev/null; [ ${#FAILED[@]} = 1 ]'
  if command -v apt-cache > /dev/null; then
    for p in $(packages "base figures pdf gpu java"); do
      ok "apt knows $p" 'apt-cache show --no-all-versions "$p" > /dev/null 2>&1'
    done
    # simulation only (-s): no root, nothing installed or changed
    # shellcheck disable=SC2046
    out=$(apt-get -s install --no-install-recommends --no-upgrade $(packages "base figures pdf gpu java") 2>&1); rc=$?
    ok "apt-get -s accepts the whole list" '[ $rc = 0 ] && ! grep -q "^E:" <<< "$out"'
    echo "     (simulation: $(grep -c '^Inst ' <<< "$out") package(s) this machine would add)"
  else echo "skip apt name checks: no apt-cache here"; fi
  # the read-only check path on this machine: its table must be complete; what this machine lacks is shown, not judged
  fx=$(mktemp)
  ( verify "base figures pdf gpu java" ) > "$fx" 2>&1; rc=$?
  ok "verify runs (rc 0 or 1)" '[ $rc = 0 ] || [ $rc = 1 ]'
  ok "verify has one dpkg row per package" '[ "$(grep -c "^dpkg " "$fx")" = "$(packages "base figures pdf gpu java" | wc -l)" ]'
  ok "verify ends with its verdict line" 'grep -q "^VERIFY \(CLEAN\|FAILED\)" "$fx"'
  sed -n 's/^  MISSING /     (this machine lacks: /p' "$fx" | sed 's/$/)/'
  rm -f "$fx"
  echo "selftest: $((n - bad)) of $n checks pass"
  [ $bad = 0 ]
}

case ${1:-} in
  --selftest) selftest ;;
  --verify) shift; set=$(profiles "${@:-base}") || exit 2; verify "$set" ;;
  "" | -h | --help) sed -n '2,8p' "$0"; exit 2 ;;
  *) set=$(profiles "$@") || exit 2; do_install "$set" || [ $? != 2 ] || exit 2; verify "$set" ;;
esac
