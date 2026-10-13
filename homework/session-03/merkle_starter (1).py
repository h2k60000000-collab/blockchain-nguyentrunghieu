#!/usr/bin/env python3
"""Lab 3.2 — Merkle tree (COMPLETED). All CHECK lines must print OK.
Implemented: merkle_root, merkle_proof, verify_proof.
"""
import hashlib
import math


def h(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def _levels(leaves: list[bytes]) -> list[list[bytes]]:
    """Return every tree level, from hashed leaves (level 0) up to the root."""
    level = [h(x) for x in leaves]
    levels = [level]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level = level + [level[-1]]            # duplicate last node (Bitcoin rule)
        level = [h(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
        levels.append(level)
    return levels


# ---- TODO 1 ---------------------------------------------------------------
def merkle_root(leaves: list[bytes]) -> bytes:
    """Build the tree bottom-up; duplicate the last node on odd levels."""
    return _levels(leaves)[-1][0]


# ---- TODO 2 ---------------------------------------------------------------
def merkle_proof(leaves: list[bytes], index: int) -> list[tuple[bytes, bool]]:
    """List of (sibling_hash, is_left) pairs from leaf to root.
    is_left=True means the sibling is the LEFT child (so it goes first when hashing)."""
    proof = []
    idx = index
    for level in _levels(leaves)[:-1]:
        if len(level) % 2 == 1:
            level = level + [level[-1]]
        if idx % 2 == 0:
            proof.append((level[idx + 1], False))   # sibling on the right
        else:
            proof.append((level[idx - 1], True))    # sibling on the left
        idx //= 2
    return proof


# ---- TODO 3 ---------------------------------------------------------------
def verify_proof(leaf_hash: bytes, proof: list[tuple[bytes, bool]], root: bytes) -> bool:
    """Recompute upward from the leaf hash and compare with the root."""
    cur = leaf_hash
    for sibling, is_left in proof:
        cur = h(sibling + cur) if is_left else h(cur + sibling)
    return cur == root


def check(name: str, ok: bool):
    print(f"  CHECK {name}: {'OK' if ok else 'FAIL'}")


if __name__ == "__main__":
    txs = [f"tx{i}".encode() for i in range(7)]          # odd count on purpose
    root = merkle_root(txs)
    print("root:", root.hex())

    check("deterministic root", root == merkle_root(txs))
    check("single leaf: root == hash(leaf)", merkle_root([b"a"]) == h(b"a"))
    check("two leaves: root == h(h(a)+h(b))", merkle_root([b"a", b"b"]) == h(h(b"a") + h(b"b")))
    check("odd level duplicates last node",
          merkle_root([b"a", b"b", b"c"]) == h(h(h(b"a") + h(b"b")) + h(h(b"c") + h(b"c"))))

    all_ok = all(verify_proof(h(txs[i]), merkle_proof(txs, i), root) for i in range(len(txs)))
    check("every leaf proof verifies", all_ok)

    p = merkle_proof(txs, 3)
    check("tampered leaf fails", not verify_proof(h(b"tx3-evil"), p, root))
    check("wrong root fails", not verify_proof(h(txs[3]), p, h(b"x")))
    check("changing one tx changes root",
          merkle_root(txs[:3] + [b"tx3-evil"] + txs[4:]) != root)

    big = [str(i).encode() for i in range(1_000_000)]
    n = 1_000_000
    print("proof length for n = 1,000,000:", math.ceil(math.log2(n)), "hashes")
    check("proof length for n=1000 is ceil(log2 n)",
          len(merkle_proof(big[:1000], 500)) == math.ceil(math.log2(1000)))
