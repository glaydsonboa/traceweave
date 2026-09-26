# Evidence signal race

The stop hook preserves the native Claude Code JSONL: it copies the bytes to a rescue file named by their
SHA-256, publishes manifest and receipt to Git, and then writes a `.ready.json` signal so an external agent
mirrors the rescue copy into a second custody location (another Windows profile).

## The failure (25/09/2026, session `8c4fa877`)

The signal step re-read the native JSONL to compute the hash. The session kept writing to that file after the
stop, so the hash changed (`f725e27a…` captured, `019836cf…` re-read). No rescue copy had the new hash, and the
hook failed with `ENOENT`. The evidence commits had already landed; only the mirror was never signaled.

## The rule

A signal about a captured artifact names **the capture**, never a fresh read of a source that is still
growing. The signal now uses the hash returned by the capture step; if the capture step failed, it signals the
newest rescue copy of the session after checking its bytes against the hash in its name. The mtime in the
signal is the rescue copy's, not the live file's.

## Evidence

Source repository `leedermix-arch/worion-desktop`: commit `9e8fc05a`. A test appends to the JSONL between the
two steps; with the old re-read it fails with the same `ENOENT`, with the fix it passes (8/8). The missing
signal for `8c4fa877` was written afterwards for the existing copy `f725e27a`, hash checked first.
