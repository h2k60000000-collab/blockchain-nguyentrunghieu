# Lab 03 — Answers

## Lab 3.1 — Hash properties & toy PoW (output)

```
SHA-256("Blockchain 2026") = c42dafbbe164b917016b4c3491ee7445e6c01fae0524a83f96c2ece8720b2d78
SHA-256("blockchain 2026") = 3b467304922f266e0331cc5e1598ec58657f48b5a9e2587763260244a30f40c7

k=1 nonce=        5 time=0.000s
k=2 nonce=       61 time=0.000s
k=3 nonce=       61 time=0.000s
k=4 nonce=    14229 time=0.013s
k=5 nonce=    55980 time=0.053s
k=6 nonce= 24517505 time=24.974s
```

Changing a single letter's case produces a completely unrelated digest (avalanche effect).

**Q1.** Each extra leading zero multiplies the expected work by **≈ 16×**. Each character of a hex digest is 4 bits, and the probability that a random hash starts with k hex zeros is 16^-k, so the expected number of attempts is 16^k. (Per *bit* it would be 2×; Bitcoin's real target works at bit granularity.) The data shows this noisily because a nonce search is random: k=6 needed ~24.5M attempts, close to 16^6 ≈ 16.8M.

**Q2.** Verifying takes **1 hash call**: compute `sha256(data + nonce)` once and check the prefix. So PoW is **asymmetric**: expensive to produce, trivial to verify. Anyone can cheaply check that real work was done, and the work cannot be faked or shortcut because SHA-256 is one-way.

## Lab 3.2 — Merkle tree

`lab03/merkle_starter.py` is completed; all CHECK lines print OK (root, odd-level duplication, proofs for every leaf, tamper detection).

**Q3.** For n = 1,000,000 transactions a proof contains **⌈log2(1,000,000)⌉ = 20 hashes** (20 × 32 bytes = 640 bytes), versus 1,000,000 hashes to recheck the whole list.

**Q4.** **Bitcoin SPV (light clients).** A light wallet downloads only block headers (80 bytes each, containing the Merkle root). To confirm that a payment is in a block, it asks a full node for the Merkle proof (the sibling hashes along the path), recomputes upward from the txid, and compares with the root in the header. It never needs the block's thousands of transactions. The same mechanism powers **Merkle-airdrop claims** (e.g. Uniswap's UNI airdrop): the contract stores only the root, and each user submits a proof of their (address, amount) leaf.

## Lab 3.3 — Sign, verify & recover (output)

```
address: 0x0833F9ef5Ae16E70A6b55705d592E9af5ac42559
r,s,v: 0xd67dee6787443a1006b92d8d22223013f32bb54eefe5c92362aee1883172cbde 0x5718bc3035268c947dfafd3fbbd06c6dec1cea8148d24ae4b259a1af5edd8389 28
second signing identical: True
recovered: 0x0833F9ef5Ae16E70A6b55705d592E9af5ac42559 | match: True
tampered -> 0x68792E98941e948A180CE25A6B76BD8496cE5797 | differs: True
```

(The key is a throwaway generated for this lab; never reuse it for real funds.)

**Task 1.** Signing the same message with the same key twice gives an **identical signature**. This is explained by **RFC 6979 (deterministic ECDSA)**: the nonce `k` is derived from the private key and the message hash via HMAC-DRBG instead of being random. (Across separate runs `Account.create()` makes a new key, so the signature differs, but for the same key and message it is always the same.) Deterministic nonces also avoid the catastrophic key leaks caused by weak or reused random `k`.

**Task 2.** The tampered message ("Buoi 4" instead of "Buoi 3") recovers a **different address** (0x6879…5797 instead of 0x0833…2559). ECDSA public-key recovery takes (message hash, r, s, v) and outputs the public key that must have produced the signature. A different message gives a different hash (avalanche effect), so the math yields an unrelated public key and address. Only the exact original bytes recover the signer's address, so a successful match proves both **who signed** (authenticity) and that the message was **not modified** (integrity).
