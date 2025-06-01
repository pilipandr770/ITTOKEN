#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для деплоя смарт-контрактов на блокчейн Polygon.
Компилирует и развертывает смарт-контракты ERC20 токена, токенсейла и DAO.
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3
from solcx import compile_standard, install_solc

# Загружаем переменные окружения из .env файла
load_dotenv()

# Устанавливаем версию solc
def install_solc_if_needed():
    """Устанавливаем компилятор Solidity если он не установлен"""
    print("Установка компилятора Solidity...")
    try:
        install_solc("0.8.19")
        print("Компилятор Solidity успешно установлен!")
    except Exception as e:
        print(f"Ошибка при установке компилятора: {e}")
        exit(1)

def compile_contract(contract_path, contract_name):
    """Компилирует смарт-контракт"""
    print(f"Компиляция контракта {contract_name}...")
    
    with open(contract_path, "r", encoding="utf-8") as file:
        contract_source = file.read()
    
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {contract_name: {"content": contract_source}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.19",
    )
    
    # Получаем ABI и байткод
    contract_data = compiled_sol["contracts"][contract_name][contract_name.split(".")[0]]
    abi = contract_data["abi"]
    bytecode = contract_data["evm"]["bytecode"]["object"]
    
    return abi, bytecode

def deploy_contract(w3, abi, bytecode, private_key, constructor_args=None):
    """Деплоит смарт-контракт в блокчейн"""
    account = w3.eth.account.from_key(private_key)
    
    # Создаем контракт
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Получаем nonce для адреса отправителя
    nonce = w3.eth.get_transaction_count(account.address)
    
    # Создаем транзакцию деплоя контракта
    if constructor_args:
        transaction = Contract.constructor(*constructor_args).build_transaction(
            {
                "chainId": w3.eth.chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": account.address,
                "nonce": nonce,
            }
        )
    else:
        transaction = Contract.constructor().build_transaction(
            {
                "chainId": w3.eth.chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": account.address,
                "nonce": nonce,
            }
        )
    
    # Подписываем транзакцию
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    
    # Отправляем транзакцию
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    
    print(f"Транзакция отправлена: {tx_hash.hex()}")
    
    # Ждем подтверждения транзакции
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt.contractAddress

def main():
    """Основная функция деплоя контрактов"""
    install_solc_if_needed()
    
    # Загружаем конфигурацию из .env
    PRIVATE_KEY = os.getenv("POLYGON_PRIVATE_KEY")
    INFURA_API_KEY = os.getenv("INFURA_API_KEY")
    
    if not PRIVATE_KEY or not INFURA_API_KEY:
        print("Необходимо указать POLYGON_PRIVATE_KEY и INFURA_API_KEY в файле .env")
        print("Формат файла .env:")
        print("POLYGON_PRIVATE_KEY=ваш_приватный_ключ")
        print("INFURA_API_KEY=ваш_ключ_infura")
        exit(1)
    
    # Настраиваем подключение к блокчейну (Mumbai Testnet)
    w3 = Web3(Web3.HTTPProvider(f"https://polygon-mumbai.infura.io/v3/{INFURA_API_KEY}"))
    
    if not w3.is_connected():
        print("Ошибка подключения к блокчейну Polygon")
        exit(1)
    
    print("Успешное подключение к блокчейну Polygon")
    
    # Пути к контрактам
    contracts_dir = Path("contracts")
    token_contract_path = contracts_dir / "ITShopToken.sol"
    
    if not token_contract_path.exists():
        print(f"Файл контракта {token_contract_path} не найден")
        exit(1)
    
    # Компилируем и деплоим токен
    token_abi, token_bytecode = compile_contract(token_contract_path, "ITShopToken.sol")
    
    # Аргументы конструктора токена: название, символ, общее предложение
    token_args = ["IT Shop Token", "ITST", 1000000 * 10**18]  # 1,000,000 токенов с 18 десятичными знаками
    
    # Деплоим токен
    print("Деплой токена...")
    token_address = deploy_contract(w3, token_abi, token_bytecode, PRIVATE_KEY, token_args)
    print(f"Токен задеплоен по адресу: {token_address}")
    
    # Сохраняем адрес и ABI контракта
    contract_data = {
        "token_address": token_address,
        "token_abi": token_abi
    }
    
    # Создаем директорию для сохранения данных контрактов, если она не существует
    deploy_dir = Path("deployments")
    deploy_dir.mkdir(exist_ok=True)
    
    with open(deploy_dir / "contract_data.json", "w") as file:
        json.dump(contract_data, file, indent=4)
    
    print("Данные контракта успешно сохранены в deployments/contract_data.json")
    
    # Обновляем .env файл с адресом контракта
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, "r") as file:
            env_content = file.read()
        
        if "CONTRACT_ADDRESS" in env_content:
            # Обновляем существующую переменную
            with open(env_path, "w") as file:
                env_content = env_content.replace(
                    f"CONTRACT_ADDRESS={env_content.split('CONTRACT_ADDRESS=')[1].split('\n')[0]}",
                    f"CONTRACT_ADDRESS={token_address}"
                )
                file.write(env_content)
        else:
            # Добавляем новую переменную
            with open(env_path, "a") as file:
                file.write(f"\nCONTRACT_ADDRESS={token_address}\n")
    else:
        # Создаем новый .env файл
        with open(env_path, "w") as file:
            file.write(f"CONTRACT_ADDRESS={token_address}\n")
    
    print("Адрес контракта добавлен в .env файл")
    print("Деплой контрактов успешно завершен!")

if __name__ == "__main__":
    main()
