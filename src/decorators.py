from __future__ import annotations

from datetime import datetime
from functools import wraps
from typing import Callable, Any
import logging

def transaction_logger(func: Callable) -> Callable:
    """
    Decorador que registra a data e hora de cada transação bancária.
    
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
