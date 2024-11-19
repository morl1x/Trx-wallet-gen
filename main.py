from tronapi import Tron
from tronapi import HttpProvider
import random
import time
import threading

# Функция для генерации случайного шестнадцатеричного приватного ключа
def generate_random_private_key():
    return ''.join([random.choice('0123456789abcdef') for _ in range(64)])


# Задаем провайдеры для HTTP и соло для Tron
full_node = HttpProvider('https://api.trongrid.io')
solidity_node = HttpProvider('https://api.trongrid.io')
event_server = HttpProvider('https://api.trongrid.io')

# Инициализируем Tron
tron = Tron(full_node=full_node,
            solidity_node=solidity_node,
            event_server=event_server)



def check_wallet_balance():
    while True:
        # Generate random private key
        private_key = generate_random_private_key()

        # Get Tron address from private key
        address = tron.address.from_private_key(private_key)

        # Check balance of the address
        try:
            balance = tron.trx.get_balance(address['base58'])
        except Exception as e:
            print(f"Error checking balance: {e}")
            continue

        print(f'Private Key: {private_key}')
        print(f'Address: {address["base58"]}')
        print(f'Balance: {balance} TRX')

        if balance > 0:
            print(f'Wallet with balance found! Private Key: {private_key}, Address: {address["base58"]}, Balance: {balance} TRX')

            # Write found wallet to file
            with open('wallets.txt', 'a') as f:
                f.write(f'PrivateKey: {private_key}\n')
                f.write(f'Address: {address["base58"]}\n')
                f.write(f'Balance: {balance} TRX\n')
                f.write('-' * 30 + '\n')

        time.sleep(0.05)

# Number of threads to run concurrently
check_wallet_balance()