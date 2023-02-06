# Ethereum

# Task 1 - Ethereum address

## a. How are Ethereum addresses generated?

Ethereum addresses are generated from:
- Last 20 bytes of Keccak-256 hash of public key
- Represented as hexadecimal number


## b. Relationship between `SHA256` and `Keccek`.

SHA-256 is implementation of SHA-2 standart with 256 bits key.

Keccak256 Cryptographic function and part of **solidity** (SHA-3 Family)

SHA-256 is weaker than Keccak-256.

## c. What is a **Ethereum Black Hole Address**

It is the genesis address of the blockchain, is hard coded and has no private key. All money that is send to this address is thus lost. "Black Hole"

## d. Idea behind **Ethereum Improvement Proposal 55**. [EIP-55: Mixed-case checksum address encoding](https://eips.ethereum.org/EIPS/eip-55#specification)

1. Convert address to hex
2. If the ith digit is a letter (abcdef) print it in uppercase if the 4*ith bit of the hash of the lowercase hexadecimal address is 1, otherwise print in lowercase.

Benefit:

- 15 check bits per address, probability that a randomly generated address if misstyped will pass a check is 0.025 %. 


## e. Generate **ETH vanity address** with Ethereum Vanity address generator.


```bash
# Address with matr. suffix
Address: 0xFcd0B52D8B83cdB6295ab58DC0033f1d3BE33975


# Address with random suffix
Address2: 0x47024D4b598095801363e4a6823B7f8da3653115

# Created via: https://vanity-eth.tk/
```



# Task 2 - Ethereum Wallet

## a. Install Ethereum wallet

Using Metamask.

## b. Default account


## c. Add new ethereum network to metamask

## d. Create vs Import account:

1. Import custom account via private key.
2. Create account with randomly generated public key.

## e. Import custom accounts.

# Task 3 - Ethereum Faucet

## a. Use ethereum faucet to send some tokens

## b. Check transaction at Ethereum Lite Explorer

Transaction hash: 0xad8bedf475a77f7358a49638a5c32fbeb181538a7f1451ba82ee26c3be95f797

## c. Whats the faucets ethereum address?

`0xB25F98E8190DaaA442Cd865f3Bfc8187C9CEaffe`

# Task 4 - Ethereum Transaction

## a. Send a small token amount to someone else

## b. Research transaction information at `Ethereum Lite Explorer`

Contains information about:

- Source / Destination address
- Time
- uncles
- Hash/Parent hash
- Nonce
- Size
- Transactions
- Sha3uncles
- Minde by
- Gas limit/ Gas used
- Difficulty
- Extra Data
- LogsBloom

## d. Send token to prof. for exam application