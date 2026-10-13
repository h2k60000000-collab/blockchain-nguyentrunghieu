# Lab 04 — Answers

## Q1 — Target & work

Block #840,000 has `bits = 0x17034219`, so target = `0x034219 × 256^20`:

```
0000000000000000000342190000000000000000000000000000000000000000
```

- The target has **about 19 leading zero hex digits** (~76 leading zero bits).
- One valid header represents about 2^256 / target ≈ **2^78** hashes (log2 ≈ 78.3), i.e. roughly 3×10^23 expected hash attempts.

## Q2 — The verify vs. find asymmetry

SHA-256 is a **one-way function (preimage resistant)** whose output behaves like a random value (avalanche effect). There is no way to work backwards or "cleverly guess" a nonce that yields a hash below the target, so the only option is **brute-force search** (~2^78 attempts). Verifying, by contrast, is just computing the hash forward over a header that already contains the winning nonce: 2 hash calls. Finding is expensive, checking is cheap.

## Q3 — The tx paying ~3.6 million sat/vB

April 20, 2024 was the day of the **4th halving** and also the **launch of the Runes protocol**. Thousands of users wanted to get into the very first block, but block space is limited (~4M weight units), so a **mempool auction** formed. The lesson: fees are **not** set by the protocol or proportional to the amount transferred; they are determined by **supply and demand for block space**. Miners pick the transactions with the highest sat/vB, so users must bid competitively to get priority. (Compare with today, where "high priority" is typically only single or double-digit sat/vB.)

## Q4 — The coinbase difference

Coinbase outputs = **block subsidy + total fees of every transaction in the block**.

4,075,061,499 − 312,500,000 = **3,762,561,499 sat ≈ 37.63 BTC**, which is the total transaction fees collected by the miner (high because of the bidding war after the halving/Runes launch described in Q3).

## Q5 — What does a matching Merkle root prove?

A recomputed Merkle root that matches the header proves the block's list of 3,050 transactions (and their order) is exactly the list the miner committed to when mining the block. Because of SHA-256's **collision resistance / second-preimage resistance** and avalanche effect, changing, adding, removing, or reordering even one transaction would change the root completely. Since the root sits in the header and the header is protected by Proof-of-Work, nobody can alter the transaction list without redoing the work for that block.
