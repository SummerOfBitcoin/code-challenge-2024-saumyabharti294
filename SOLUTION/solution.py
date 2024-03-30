import os
import json

# Define the folder path where JSON files are located
folder_path = "mempool"

# Maximum weight for a block
maxweight = 4000000.0

# Define the Transaction class to represent transactions
class Transaction:
    def __init__(self):
        self.tx_id = ""      # Transaction ID
        self.parents = []    # List of parent transaction IDs
        self.fee = 0         # Transaction fee
        self.weight = 0      # Transaction weight

# Function to create Transaction objects from JSON data
def createTransaction(data):
    ans = Transaction()
    ans.tx_id = data['vin'][0]['txid']
    ans.fee = data['vout'][0]['value']
    ans.weight = data['vout'][0]['value']  # Assuming weight is the same as value
    ans.parents = [vin['txid'] for vin in data['vin']]
    return (ans.tx_id, ans)

# Function to read JSON files and create Transaction objects
def readJSON(fileName):
    umap = {}
    with open(fileName, 'r') as file:
        data = json.load(file)
        p = createTransaction(data)
        umap[p[0]] = p[1]
    print("Total number of transactions read:", len(umap))
    return umap

# Function to check if a transaction is valid based on its parents
def isValidTx(tx, included_tx_set):
    for parent in tx.parents:
        if parent not in included_tx_set:
            return False
    return True

# Function to write included transactions to a file
def writeOutput(included_tx_vector, fn):
    with open(fn, 'w') as file:
        for s in included_tx_vector:
            file.write(s + '\n')

# Function to generate a block from JSON file
def generateBlock(file_path):
    umap = readJSON(file_path)
    tx_set = set() 
    included_tx_set = set()                                                 
    included_tx_vector = []                                           
    for tx in umap.values():
        if tx.weight == 0:
            continue
        tx_set.add(((tx.fee / tx.weight), tx))
    currBlockWeight = 0.0
    totalFee = 0
    while tx_set and currBlockWeight < maxweight:
        found = False
        for tx in sorted(tx_set, reverse=True, key=lambda x: x[0]):
            curr_tx = tx[1]
            currFee = curr_tx.fee
            currWeight = curr_tx.weight
            if isValidTx(curr_tx, included_tx_set) and (currBlockWeight + currWeight) <= maxweight:
                currBlockWeight += currWeight
                included_tx_set.add(curr_tx.tx_id)
                included_tx_vector.append(curr_tx.tx_id)
                totalFee += currFee
                tx_set.remove(tx)
                found = True
                break
        if not found:
            break
    block_header = f"Processing: {file_path}\nTotal number of transactions read: {len(umap)}\nNumber of tx in final block: {len(included_tx_set)}\nTotal fee in curr block: {totalFee}\nTotal weight: {currBlockWeight}\nPercentage of weight: {(currBlockWeight / maxweight) * 100}%"
    coinbase_tx = umap[list(umap.keys())[0]].tx_id  # Assuming the first transaction is the coinbase transaction
    return block_header, coinbase_tx, included_tx_vector

# Function to generate block header
def generateBlockHeader(block_header, coinbase_tx, included_tx_vector):
    block_header += f"\nCoinbase Transaction: {coinbase_tx}\n"
    block_header += "Included Transactions:\n"
    for txid in included_tx_vector:
        block_header += f"- {txid}\n"
    return block_header

if __name__ == "__main__":
    # Iterate through JSON files in folder_path
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            print("Processing:", file_path)
            # Generate block information
            block_header, coinbase_tx, included_tx_vector = generateBlock(file_path)
            # Generate block header
            block_header = generateBlockHeader(block_header, coinbase_tx, included_tx_vector)
            # Write block header to output.txt
            with open("output.txt", 'a') as file:
                file.write(block_header + '\n')
            umap = readJSON(file_path)
            tx_set = set() 
            included_tx_set = set()                                                 
            included_tx_vector = []                                           
            for tx in umap.values():
             if tx.weight == 0:
               continue
             tx_set.add(((tx.fee / tx.weight), tx))
            currBlockWeight = 0.0
            totalFee = 0
            while tx_set and currBlockWeight < maxweight:
                found = False
                for tx in sorted(tx_set, reverse=True, key=lambda x: x[0]):
                    curr_tx = tx[1]
                    currFee = curr_tx.fee
                    currWeight = curr_tx.weight
                    if isValidTx(curr_tx, included_tx_set) and (currBlockWeight + currWeight) <= maxweight:
                        currBlockWeight += currWeight
                        included_tx_set.add(curr_tx.tx_id)
                        included_tx_vector.append(curr_tx.tx_id)
                        totalFee += currFee
                        tx_set.remove(tx)
                        found = True
                        break
                if not found:
                    break
            print("Number of tx in final block:", len(included_tx_set))
            print("Total fee in curr block:", totalFee)
            print("Total weight:", currBlockWeight)
            percentage = (currBlockWeight / maxweight) * 100.0
            print("Percentage of weight:", percentage, "%")
            print()
            writeOutput(included_tx_vector, "block.txt")
