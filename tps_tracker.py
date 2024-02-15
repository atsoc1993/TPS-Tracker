from algosdk.v2client import algod
import time

'''
DEPENDING ON YOUR PROCESSING SPEED, BLOCKS MIGHT BE SKIPPED AND SLEEP TIME SHOULD BE ADJUSTED
'''

#Include your node token and port below
algod_token = '' 
algod_port = ''

last_block_time_stamp = 0
last_tracked_block = 0
inner_transactions = 0
outer_transactions = 0
while True:
    algod_client = algod.AlgodClient(algod_token, algod_port)
    last_block = algod_client.status()['last-round']
    if last_tracked_block != last_block:
        current_block_time_stamp = algod_client.block_info(last_block)['block']['ts']
        last_tracked_block = last_block
        last_block_txs = algod_client.get_block_txids(last_block)['blockTxids']
        for tx in last_block_txs:
            tx_info = algod_client.pending_transaction_info(tx)
            outer_transactions += 1
            #if 'grp' in tx_info['txn']['txn']:
               # print(tx_info['txn']['txn']['grp'])
              #  print(tx)
             #   print('\n')
            if 'inner-txns' in tx_info:
                total_inner_in_tx = len(tx_info['inner-txns'])
                inner_transactions += 1
        outer_only_tx_per_s_avg = (outer_transactions) / (current_block_time_stamp - last_block_time_stamp)
        outer_inner_tx_per_s_avg = (outer_transactions + inner_transactions) / (current_block_time_stamp - last_block_time_stamp)
        if last_block_time_stamp != 0:
            print(f'Block: {last_block}: \nOuter Transactions: {outer_transactions}\nInner Transactions: {inner_transactions}\nTPS w/o Inner Tx: {outer_only_tx_per_s_avg:.0f} Tx/s\nTPS w/ Inner Txs: {outer_inner_tx_per_s_avg:.0f} Tx/s\n')
        last_block_time_stamp = algod_client.block_info(last_block)['block']['ts']
        inner_transactions = 0
        outer_transactions = 0
    time.sleep(1)
