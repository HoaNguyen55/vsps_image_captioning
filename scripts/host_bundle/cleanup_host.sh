#!/bin/bash
# Laptop clean-up after a rented host is deleted (PI-1115s): every file about the machine goes, except logs.
#   bash cleanup_host.sh <alias> --dry-run   list what would be removed; changes nothing
#   bash cleanup_host.sh <alias>             remove it, then print one OPS text (names only, never an address)
# Run it only after the delete on the panel and L-after. Removed: the alias's block in the ssh client config, its
# host keys (ssh-keygen -R for the alias, the address, the port form and any HostKeyAlias), a per-host known_hosts
# file, its control socket, askpass/password files and pid files whose name carries the alias. Kept: the LOG, the
# session record folders (logs, sums, pulled results), *.log files and everything inside a git work tree.
# Overrides for a test tree: SSH_DIR (default ~/.ssh), PRIV_DIRS (folders searched, depth 1, for askpass,
# password and pid files; default "~/.config/vsps ~ /tmp").
set -u -o pipefail
A=${1:-}; MODE=${2:-}
case $A in "" | -*) sed -n '2,10p' "$0"; exit 2 ;; esac
case $A in *[!A-Za-z0-9_-]*) echo "alias must be letters, digits, _ or -"; exit 2 ;; esac
case $MODE in "" | --dry-run) ;; *) echo "unknown option: $MODE"; exit 2 ;; esac
SSH_DIR=${SSH_DIR:-$HOME/.ssh}; CFG=$SSH_DIR/config
PRIV_DIRS=${PRIV_DIRS:-$HOME/.config/vsps $HOME /tmp}
DRY=0; [ "$MODE" = --dry-run ] && DRY=1
DONE=()

act() {  # act <what, names only> <command...>: runs it unless --dry-run; records the name either way
  local what=$1; shift
  [ -n "${HN:-}" ] && what=${what//"$HN"/HOST}                                    # never the host's name or address,
  what=$(sed -E 's/([0-9]{1,3}\.){3}[0-9]{1,3}/ADDRESS/g' <<< "$what")             # not even inside a file name
  if [ $DRY = 1 ]; then echo "would remove: $what"
  elif "$@"; then echo "removed: $what"
  else echo "FAILED: $what"; return 1; fi
  DONE+=("$what")
}
in_block() {  # awk program: prints the config without (mode drop) or counts (mode count) the alias's Host block
  awk -v a="$A" -v mode="$1" '
    /^[ \t]*(Host|Match)[ \t]/ { inb = 0
      if (tolower($1) == "host") for (i = 2; i <= NF; i++) if ($i == a) { inb = 1; names = NF - 1 } }
    inb { c++ } !inb && mode == "drop" { print }
    END { if (mode == "count" && c) print c, names }' "$CFG"
}
drop_key() { ssh-keygen -R "$1" -f "$2" > /dev/null 2>&1 && rm -f "$2.old"; }   # the .old copy would keep the entry
drop_block() {  # rewrite the config without the block, mode 600
  local t; t=$(mktemp "$CFG.XXXXXX") || return 1
  in_block drop > "$t" && chmod 600 "$t" && mv "$t" "$CFG"
}

# 1. what the ssh client knows about the alias: kept in variables, never printed
blk=""; HN=""; PORT=""; HKA=""; CP=""; KH=""
[ -f "$CFG" ] && blk=$(in_block count)
if [ -z "$blk" ]; then echo "no 'Host $A' block in $CFG"; else
  read -r NLINES NNAMES <<< "$blk"
  [ "$NNAMES" = 1 ] || { echo "STOP: the Host line of $A names other aliases too; edit $CFG by hand"; exit 1; }
  G=$(ssh -F "$CFG" -G "$A" < /dev/null 2> /dev/null)
  HN=$(awk '$1 == "hostname" {print $2}' <<< "$G"); PORT=$(awk '$1 == "port" {print $2}' <<< "$G")
  HKA=$(awk '$1 == "hostkeyalias" {print $2}' <<< "$G"); CP=$(awk '$1 == "controlpath" {print $2}' <<< "$G")
  KH=$(awk '$1 == "userknownhostsfile" {for (i = 2; i <= NF; i++) print $i}' <<< "$G")
fi

# 2. host keys in the default known_hosts files and in the alias's own ones
for f in $(printf '%s\n' "$SSH_DIR/known_hosts" "$SSH_DIR/known_hosts2" $KH | sort -u); do
  [ -f "$f" ] || continue
  for k in "$A" ${HN:+"$HN"} ${HN:+"[$HN]:${PORT:-22}"} ${HKA:+"$HKA"}; do
    ssh-keygen -F "$k" -f "$f" > /dev/null 2>&1 && act "host key of $A in $(basename "$f")" drop_key "$k" "$f"
  done
done
# a per-host known_hosts file: only a file whose name carries the alias as a whole part. Any other UserKnownHostsFile
# (the default ones, a file shared with other hosts) keeps its other entries: step 2 removed this host's keys from it.
for f in $(printf '%s\n' "$SSH_DIR/known_hosts_$A" $KH | sort -u); do
  basename "$f" | grep -q -E "(^|[^A-Za-z0-9])$A([^A-Za-z0-9]|\$)" || continue
  [ -f "$f" ] && act "per-host known_hosts file $(basename "$f")" rm -f "$f"
done

# 3. control sockets
[ -n "$CP" ] && [ "$CP" != none ] && [ -S "$CP" ] && act "control socket $(basename "$CP")" rm -f "$CP"
for f in "$SSH_DIR"/*"$A"*; do [ -S "$f" ] && [ "$f" != "$CP" ] && act "control socket $(basename "$f")" rm -f "$f"; done

# 4. askpass, password and pid files whose name carries the alias as a whole part
for d in $PRIV_DIRS; do
  [ -d "$d" ] || continue
  while IFS= read -r f; do
    basename "$f" | grep -q -E "(^|[^A-Za-z0-9])$A([^A-Za-z0-9]|$)" || continue
    git -C "$(dirname "$f")" rev-parse --is-inside-work-tree > /dev/null 2>&1 && continue
    if [ "${f##*.}" = pid ] && kill -0 "$(head -c 20 "$f" | tr -cd 0-9)" 2> /dev/null; then
      echo "KEPT: pid file $(basename "$f") names a live process; stop it by the skill's rule first"; continue
    fi
    act "file $(basename "$f") in $d" rm -f "$f"
  done < <(find "$d" -maxdepth 1 \( -type f -o -type l \) ! -name '*.log' \
             \( -name "*askpass*$A*" -o -name "*$A*askpass*" -o -name "*pass*$A*" -o -name "*$A*pass*" \
                -o -name "*pw*$A*" -o -name "*$A*pw*" -o -name "*$A*.pid" \) 2> /dev/null | sort)
done

# 5. the config block last (steps 1 to 3 read it)
[ -n "$blk" ] && act "the 'Host $A' block of $(basename "$CFG") ($NLINES lines)" drop_block

[ ${#DONE[@]} = 0 ] && DONE=("nothing found")
pre=removed; [ $DRY = 1 ] && pre="would remove (dry run)"
echo
echo "OPS text: host clean-up $A (PI-1115s) | $pre: $(printf '%s; ' "${DONE[@]}" | sed 's/; $//') | kept: LOG lines, session record folders, *.log"
