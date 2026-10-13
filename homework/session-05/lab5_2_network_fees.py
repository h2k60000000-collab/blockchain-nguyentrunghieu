# ==========================================
# LAB 5.2 - NETWORK FEES
# TrustKeys L1 Testnet
# ==========================================
# pip install web3
from web3 import Web3

# RPC of TrustKeys L1 Testnet
RPC_URL = "https://l1testnet.trustkeys.network"

# Replace with your MetaMask address (leave as-is to skip the balance step)
ADDRESS = "YOUR_WALLET_ADDRESS"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ==========================================
# 1. CHECK CONNECTION
# ==========================================
print("==========================================")
print("       TRUSTKEYS L1 TESTNET")
print("==========================================")

if not w3.is_connected():
    print("❌ Connection failed!")
    raise SystemExit(1)

print("✅ Connected to TrustKeys L1 Testnet")
print("Chain ID:", w3.eth.chain_id)

# ==========================================
# 2. GET WALLET BALANCE (eth_getBalance)
# ==========================================
print("\n==========================================")
print("              WALLET BALANCE")
print("==========================================")

if ADDRESS != "YOUR_WALLET_ADDRESS":
    balance_wei = w3.eth.get_balance(Web3.to_checksum_address(ADDRESS))
    print("Wallet:", ADDRESS)
    print("Balance:", balance_wei, "wei")
    print("Balance:", w3.from_wei(balance_wei, "ether"), "TRUSTK")
else:
    print("No MetaMask address entered.")

# ==========================================
# 3. GET LATEST BLOCK (eth_getBlockByNumber)
# ==========================================
print("\n==========================================")
print("             LATEST BLOCK")
print("==========================================")

latest_block_number = w3.eth.block_number
print("Latest block:", latest_block_number)

block = w3.eth.get_block(latest_block_number)
print("Block number:", block.number)
print("Block hash:", block.hash.hex())
print("Timestamp:", block.timestamp)
print("Number of transactions:", len(block.transactions))

# ==========================================
# 4. GET FEE HISTORY (eth_feeHistory)
# ==========================================
print("\n==========================================")
print("             FEE HISTORY")
print("==========================================")

fee_history = w3.eth.fee_history(20, "latest", [50])
oldest = fee_history["oldestBlock"]

# eth_feeHistory returns N+1 baseFeePerGas values: the N requested blocks
# PLUS the projected base fee of the NEXT block. gasUsedRatio has only N.
all_base_fees = fee_history["baseFeePerGas"]
base_fees = all_base_fees[:-1]          # the 20 real blocks
next_base_fee = all_base_fees[-1]       # projection for the next block

# ==========================================
# 5. PRINT LAST 20 BASE FEES
# ==========================================
print("\nLast 20 Base Fees:")
for i, fee in enumerate(base_fees):
    print(f"Block {oldest + i}: {fee} wei | {w3.from_wei(fee, 'gwei')} Gwei")

print(f"Next block (projected): {next_base_fee} wei | "
      f"{w3.from_wei(next_base_fee, 'gwei')} Gwei")

# ==========================================
# 6. GAS USED RATIO
# ==========================================
print("\n==========================================")
print("             GAS USED RATIO")
print("==========================================")

gas_used_ratios = fee_history["gasUsedRatio"]
for i, ratio in enumerate(gas_used_ratios):
    print(f"Block {oldest + i}: {ratio:.4f} ({ratio * 100:.2f}%)")

# ==========================================
# 7. AVERAGE BASE FEE
# ==========================================
print("\n==========================================")
print("            FEE ANALYSIS")
print("==========================================")

average_base_fee = sum(base_fees) / len(base_fees)
average_base_fee_gwei = w3.from_wei(int(average_base_fee), "gwei")
print("Average Base Fee:", average_base_fee_gwei, "Gwei")

# ==========================================
# 8. AVERAGE GAS USAGE
# ==========================================
average_gas_usage = sum(gas_used_ratios) / len(gas_used_ratios)
print("Average Gas Usage:", f"{average_gas_usage * 100:.2f}%")

# ==========================================
# 9. NETWORK STATUS
# (EIP-1559 targets 50% full blocks: above that the base fee rises,
#  below it the base fee falls.)
# ==========================================
if average_gas_usage > 0.70:
    status = "BUSY"
elif average_gas_usage > 0.30:
    status = "MODERATE"
else:
    status = "NOT BUSY"
print("Network Status:", status)

# ==========================================
# 10. FINAL SUMMARY
# ==========================================
print("\n==========================================")
print("               SUMMARY")
print("==========================================")
print("RPC:", RPC_URL)
print("Chain ID:", w3.eth.chain_id)
print("Latest Block:", latest_block_number)
print("Average Base Fee:", average_base_fee_gwei, "Gwei")
print("Average Gas Usage:", f"{average_gas_usage * 100:.2f}%")
print("Network Status:", status)
print("==========================================")
