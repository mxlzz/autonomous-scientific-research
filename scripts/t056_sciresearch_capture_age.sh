#!/usr/bin/env bash
# T0.56: collect the four final SciResearch JSON outputs from an ORIGINAL
# run_dir, ignoring error.txt/running.lock, then encrypt without public plaintext.
# Intended to execute AFTER the original grader/writer and BEFORE evaluator cleanup.
set -Eeuo pipefail
set +x
umask 077
fail() { printf 'T056_FAIL_CLOSED\n' >&2; exit 2; }
[[ $# -eq 3 ]] || fail
run_dir=$1
artifact_dir=$2
recipient=$3
[[ -d "$run_dir" && ! -L "$run_dir" && -d "$artifact_dir" && ! -L "$artifact_dir" ]] || fail
command -v realpath >/dev/null 2>&1 || fail
source_real=$(realpath -e -- "$run_dir") || fail
dest_real=$(realpath -e -- "$artifact_dir") || fail
[[ "$source_real" != "$dest_real" ]] || fail
case "$dest_real" in "$source_real"/*) fail ;; esac
case "$source_real" in "$dest_real"/*) fail ;; esac
[[ ! -e "$artifact_dir/trace.age" && ! -L "$artifact_dir/trace.age" ]] || fail
for f in transcript.json env_trace.json state_log.json result.json; do
  [[ -f "$run_dir/$f" && ! -L "$run_dir/$f" ]] || fail
done
temp=$(mktemp -d "$artifact_dir/.t056.XXXXXXXX") || fail
trap 'rm -rf -- "$temp"' EXIT
mkdir -m 700 -- "$temp/source" || fail
for f in transcript.json env_trace.json state_log.json result.json; do
  cp -- "$run_dir/$f" "$temp/source/$f" >/dev/null 2>&1 || fail
  [[ -f "$temp/source/$f" && ! -L "$temp/source/$f" ]] || fail
done
wrapper=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/t054_age_trace_archive.sh
[[ -f "$wrapper" ]] || fail
bash "$wrapper" "$temp/source" "$temp/trace.age" "$recipient" >/dev/null 2>&1 || fail
[[ -s "$temp/trace.age" ]] || fail
# Validate the encrypted stream, never print source file names or data.
[[ $(head -c 21 "$temp/trace.age") == "age-encryption.org/v1" ]] || fail
mv --no-clobber -- "$temp/trace.age" "$artifact_dir/trace.age" || fail
[[ -s "$artifact_dir/trace.age" ]] || fail
printf 'T056_CAPTURE_ENCRYPT_OK\n'
