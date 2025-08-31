from __future__ import annotations

from datetime import datetime
from functools import wraps
from typing import Callable, Any
import logging
import json
import os

def save_to_log_file(log_data: dict) -> None:
    """
    Salva os dados de log em um arquivo log.txt.
    
    Args:
        log_data (dict): Dicionário com os dados do log
    """
    try:
        # Converte os dados para JSON em uma linha
        log_line = json.dumps(log_data, ensure_ascii=False)
        
        # Abre o arquivo em modo append (adiciona ao final)
        with open('log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_line + '\n')
            
    except Exception as e:
        # Se houver erro ao salvar o log, apenas imprime no console
        print(f"⚠️  Erro ao salvar log em arquivo: {str(e)}")

def transaction_logger(func: Callable) -> Callable:
    """
    Decorador que registra a data e hora de cada transação bancária.
    Salva as informações em arquivo log.txt e também exibe no console.
    
    Args:
        func (Callable): Função a ser decorada (método execute das transações)
        
    Returns:
        Callable: Função decorada com logging de transação
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Obtém a instância da transação (primeiro argumento após self)
        transaction_instance = args[0] if args else None
        
        # Registra o início da transação
        start_time = datetime.now()
        transaction_type = type(transaction_instance).__name__
        
        # Armazena o timestamp na transação para uso posterior
        transaction_instance._timestamp = start_time
        
        # Prepara dados para o log
        log_data = {
            'timestamp': start_time.strftime('%d/%m/%Y às %H:%M:%S'),
            'function_name': func.__name__,
            'transaction_type': transaction_type,
            'arguments': {
                'args': [str(arg) for arg in args[1:]],  # Exclui self
                'kwargs': {k: str(v) for k, v in kwargs.items()}
            }
        }
        
        # Adiciona informações específicas da transação
        if hasattr(transaction_instance, 'value'):
            log_data['transaction_value'] = str(transaction_instance.value)
        
        if hasattr(transaction_instance, 'account'):
            log_data['account_number'] = str(transaction_instance.account.account_number)
            log_data['client_name'] = transaction_instance.account.client.name
        
        if hasattr(transaction_instance, 'destination_account'):
            log_data['destination_account'] = str(transaction_instance.destination_account.account_number)
            log_data['destination_client'] = transaction_instance.destination_account.client.name
        
        # Exibe no console (mantém o comportamento original)
        print(f"\n{'='*60}")
        print(f"🕐 INÍCIO DA TRANSAÇÃO: {transaction_type}")
        print(f"📅 Data/Hora: {start_time.strftime('%d/%m/%Y às %H:%M:%S')}")
        print(f"💰 Valor: R$ {transaction_instance.value if hasattr(transaction_instance, 'value') else 'N/A'}")
        
        if hasattr(transaction_instance, 'account'):
            print(f"🏦 Conta: {transaction_instance.account.account_number}")
            print(f"👤 Cliente: {transaction_instance.account.client.name}")
        
        # Para transferências, mostra informações da conta de destino
        if hasattr(transaction_instance, 'destination_account'):
            print(f"🎯 Conta Destino: {transaction_instance.destination_account.account_number}")
            print(f"👤 Cliente Destino: {transaction_instance.destination_account.client.name}")
        
        print(f"{'='*60}")
        
        try:
            # Executa a transação
            result = func(*args, **kwargs)
            
            # Registra o sucesso da transação
            end_time = datetime.now()
            duration = end_time - start_time
            
            # Atualiza dados do log com resultado
            log_data['return_value'] = str(result)
            log_data['status'] = 'Sucesso'
            log_data['duration_seconds'] = duration.total_seconds()
            log_data['end_timestamp'] = end_time.strftime('%d/%m/%Y às %H:%M:%S')
            
            # Salva no arquivo de log
            save_to_log_file(log_data)
            
            # Exibe no console
            print(f"\n{'='*60}")
            print(f"✅ TRANSAÇÃO CONCLUÍDA: {transaction_type}")
            print(f"📅 Data/Hora: {end_time.strftime('%d/%m/%Y às %H:%M:%S')}")
            print(f"⏱️  Duração: {duration.total_seconds():.2f} segundos")
            print(f"🎯 Status: {'Sucesso' if result else 'Falha'}")
            print(f"{'='*60}\n")
            
            return result
            
        except Exception as e:
            # Registra o erro da transação
            end_time = datetime.now()
            duration = end_time - start_time
            
            # Atualiza dados do log com erro
            log_data['return_value'] = None
            log_data['status'] = 'Erro'
            log_data['error_message'] = str(e)
            log_data['duration_seconds'] = duration.total_seconds()
            log_data['end_timestamp'] = end_time.strftime('%d/%m/%Y às %H:%M:%S')
            
            # Salva no arquivo de log
            save_to_log_file(log_data)
            
            # Exibe no console
            print(f"\n{'='*60}")
            print(f"❌ ERRO NA TRANSAÇÃO: {transaction_type}")
            print(f"📅 Data/Hora: {end_time.strftime('%d/%m/%Y às %H:%M:%S')}")
            print(f"⏱️  Duração: {duration.total_seconds():.2f} segundos")
            print(f"🚨 Erro: {str(e)}")
            print(f"{'='*60}\n")
            
            # Re-lança a exceção para manter o comportamento original
            raise
    
    return wrapper

def transaction_timestamp(func: Callable) -> Callable:
    """
    Decorador simples que apenas adiciona timestamp à transação.
    
    Args:
        func (Callable): Função a ser decorada
        
    Returns:
        Callable: Função decorada com timestamp
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Adiciona timestamp à instância da transação
        transaction_instance = args[0] if args else None
        if transaction_instance:
            transaction_instance._timestamp = datetime.now()
        
        return func(*args, **kwargs)
    
    return wrapper
