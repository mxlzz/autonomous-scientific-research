#!/usr/bin/env bash
# T0.54: encrypt only four SciResearch trace files to an age public recipient.
set -Eeuo pipefail
set +x
umask 077
fail() { printf 'T054_FAIL_CLOSED\n' >&2; exit 2; }
[[ $# -eq 3 ]] || fail
src=$1
dst=$2
recipient=$3
command -v tar >/dev/null 2>&1 || fail
command -v age >/dev/null 2>&1 || fail
command -v realpath >/dev/null 2>&1 || fail
[[ -d "$src" && ! -L "$src" && -n "$recipient" && ! -e "$dst" ]] || fail
destdir=$(dirname -- "$dst")
[[ -d "$destdir" ]] || fail
src_real=$(realpath -e -- "$src") || fail
dst_real=$(realpath -m -- "$dst") || fail
case "$dst_real" in "$src_real"/*|"$src_real") fail ;; esac
expected=(transcript.json env_trace.json state_log.json result.json)
for entry in "$src"/* "$src"/.[!.]* "$src"/..?*; do
    [[ -e "$entry" || -L "$entry" ]] || continue
    basename=$(basename -- "$entry")
    allowed=false
    for item in "${expected[@]}"; do
        if [[ "$basename" == "$item" ]]; then allowed=true; break; fi
    done
    [[ "$allowed" == true && -f "$entry" && ! -L "$entry" ]] || fail
done
for item in "${expected[@]}"; do
    [[ -f "$src/$item" && ! -L "$src/$item" ]] || fail
done
tmp=$(mktemp -d "$destdir/.t054.XXXXXXXX") || fail
trap 'rm -rf -- "$tmp"' EXIT
chmod 700 -- "$tmp" || fail
if ! (set -o pipefail; tar --format=ustar --owner=0 --group=0 --numeric-owner -C "$src" -cf - "${expected[@]}" 2>/dev/null | age -r "$recipient" -o "$tmp/trace.age" >/dev/null 2>&1); then fail; fi
[[ -s "$tmp/trace.age" ]] || fail
[[ $(head -c 21 "$tmp/trace.age") == 'age-encryption.org/v1' ]] || fail
chmod 600 -- "$tmp/trace.age" || fail
mv --no-clobber -- "$tmp/trace.age" "$dst" || fail
[[ -s "$dst" ]] || fail
printf 'T054_ENCRYPT_OK\n'
