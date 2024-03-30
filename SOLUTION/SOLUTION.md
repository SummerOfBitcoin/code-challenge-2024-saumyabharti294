## Mempool Block Generator

This Python script processes transactions stored in JSON files in the `mempool` folder and generates block headers along with the list of included transactions. It ensures that the total weight of transactions in a block does not exceed the specified maximum weight.

### Prerequisites

- Python 3.x
- JSON files containing transaction data in the following format:

```json
{
  "version": 2,
  "locktime": 834431,
  "vin": [
    {
      "txid": "transaction_id",
      ...
    },
    ...
  ],
  "vout": [
    {
      "scriptpubkey": "output_script",
      ...
    },
    ...
  ]
}
```

### How to Run

1. Clone the repository:

```bash
git clone https://github.com/your-username/mempool-block-generator.git
```

2. Navigate to the project directory:

```bash
cd mempool
```

3. Place your JSON files containing transaction data inside the `mempool` folder.
4. Place the solution.py script inside the mempool folder containing all the JSON files.

5. Execute the script:

```bash
python mempool/solution.py
```

For windows user : run.bat file is used to run the code

For Mac Users : run.sh file is used to run the code


5. Check the `output.txt` file generated in the project directory for the block headers and included transactions.

### Output Format

The output file `output.txt` will contain block headers and included transactions for each processed JSON file. Each block is separated by an empty line.

Example output format:

```
Processing: mempool/transaction1.json
Total number of transactions read: 10
Number of tx in final block: 5
Total fee in curr block: 200000
Total weight: 3000000.0
Percentage of weight: 75.0%
Coinbase Transaction: coinbase_transaction_id
Included Transactions:
- included_transaction_id_1
- included_transaction_id_2
...
```



![image](https://github.com/SummerOfBitcoin/code-challenge-2024-saumyabharti294/assets/101875584/a958f589-42ef-4bb0-ace0-b49d4fcb7e21)




### Notes

- The script assumes that the first transaction in each JSON file is the coinbase transaction.
- The maximum weight for a block is set to 4000000.0.
- Transactions are included in the block based on their fee/weight ratio, prioritizing transactions with higher fee/weight ratios.

### Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements or suggestions.

### License

This project is licensed under the [MIT License](LICENSE).
