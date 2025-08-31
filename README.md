
# 💰 Sistema Bancário em Python

Projeto de um sistema bancário orientado a objetos, que permite ao usuário criar contas, realizar operações como depósito, saque, transferências entre contas e visualizar extratos. O sistema implementa o padrão Strategy para transações bancárias.

## 📂 Estrutura do Projeto

```
DIO-Projeto-Sistema-Bancario/
├── index.py                 # Arquivo principal que inicia a execução do sistema
├── src/
│   ├── __init__.py          # Configurações de importação do módulo src
│   ├── Bank.py              # Gerencia clientes e suas contas bancárias
│   ├── Utils.py             # Utilidades como arredondamento e limpeza do terminal
│   ├── decorators.py        # Decoradores para logging de transações
│   └── entities/            # Entidades do sistema bancário
│       ├── __init__.py      # Configurações de importação das entidades
│       ├── Account.py       # Classe principal para contas bancárias
│       ├── Transaction.py   # Classe abstrata para transações bancárias
│       ├── Deposit.py       # Implementação de transação de depósito
│       ├── Withdraw.py      # Implementação de transação de saque
│       ├── Transfer.py      # Implementação de transação de transferência
│       ├── Client.py        # Define o cliente com dados pessoais
│       ├── AccountNumber.py # Validação e geração de números de conta
│       ├── AgencyNumber.py  # Validação e geração de números de agência
│       ├── CPF.py           # Validação e formatação de CPF
│       ├── Address.py       # Endereço do cliente
│       └── DateOfBirth.py   # Data de nascimento do cliente
└── README.md               # Este arquivo
```

## 🏗️ Arquitetura

O sistema foi refatorado para implementar o **padrão Strategy** para transações bancárias:

### Classes Principais

- **`Account`**: Classe concreta que representa uma conta bancária com todas as funcionalidades
- **`Transaction`**: Classe abstrata que define a interface para transações bancárias
- **`Deposit`**: Implementação específica para transações de depósito
- **`Withdraw`**: Implementação específica para transações de saque
- **`Transfer`**: Implementação específica para transações de transferência entre contas

### Padrão Strategy Implementado

As operações de depósito, saque e transferência agora são delegadas para classes especializadas:
- `Account.deposit()` → `Deposit.execute()`
- `Account.withdraw()` → `Withdraw.execute()`
- `Account.transfer()` → `Transfer.execute()`

Isso permite maior flexibilidade e facilita a adição de novos tipos de transações no futuro.

## 🚀 Como Executar

1. Certifique-se de que o Python 3.8+ está instalado
2. Navegue até a pasta do projeto
3. Execute o sistema com:

```bash
python index.py
```

## 🧠 Funcionalidades

### Operações Básicas
- ✅ Cadastro de cliente com validação de CPF
- ✅ Criação de conta bancária
- ✅ Login via CPF e número da conta
- ✅ Depósito com validações
- ✅ Saque com validações e limites
- ✅ Transferência entre contas
- ✅ Extrato detalhado com timestamp

### Validações Implementadas
- ✅ CPF no formato válido `000.000.000-00`
- ✅ Validação de endereço completo
- ✅ Validação de data de nascimento
- ✅ Validação de números de conta e agência

## ✅ Regras de Negócio

### Limites de Saque
- **Saque máximo por operação**: R$ 500,00
- **Máximo de saques por sessão**: 3 saques
- **Validação de saldo**: Não permite saque maior que o saldo disponível

### Validações Gerais
- **Depósitos**: Apenas valores positivos
- **Transferências**: Não permite transferir para a mesma conta
- **CPF**: Deve ser único no sistema
- **Contas**: Números de conta e agência são únicos

## 🔧 Melhorias Implementadas

### 1. Padrão Strategy para Transações
- Separação clara entre lógica de conta e lógica de transação
- Facilita manutenção e extensão do código
- Melhor organização do código

### 2. Simplificação da Hierarquia de Classes
- Remoção da classe `CheckingAccount`
- `Account` agora é uma classe concreta com todas as funcionalidades
- Código mais limpo e direto

### 3. Melhor Tratamento de Erros
- Validações específicas para cada tipo de transação
- Mensagens de erro mais claras e informativas
- Tratamento robusto de exceções

### 4. Interface Visual Melhorada
- Feedback visual durante processamento de transações
- Mensagens de confirmação claras
- Formatação consistente de valores monetários

### 5. Sistema de Transações com Lista de Objetos
- **Substituição do extrato por lista de transações**: O extrato agora é gerado dinamicamente a partir de uma lista de objetos `Transaction`
- **Classe Transfer dedicada**: Criada uma classe específica para transferências entre contas
- **Melhor rastreabilidade**: Cada transação é um objeto com informações completas
- **Extrato mais preciso**: O saldo é calculado corretamente após cada transação
- **Flexibilidade**: Fácil adição de novos tipos de transação no futuro

### 6. Decorador de Logging de Transações
- **Decorador `@transaction_logger`**: Aplicado a todos os métodos `execute()` das transações
- **Registro completo**: Data/hora de início, duração, status e informações detalhadas
- **Timestamp armazenado**: Cada transação armazena seu timestamp para uso no extrato
- **Logging visual**: Interface clara com emojis e formatação para facilitar o acompanhamento
- **Tratamento de erros**: Captura e exibe erros durante a execução das transações

## 📊 Exemplo de Uso

```python
# Criação de cliente
from src.entities import Client, CPF, DateOfBirth, Address
from src.entities import Account, AccountNumber, AgencyNumber

# Criar cliente
cpf = CPF("123.456.789-00")
date_of_birth = DateOfBirth("01/01/1990")
address = Address("Rua Exemplo", "123", "Centro", "Cidade", "Estado")
client = Client("João Silva", cpf, date_of_birth, address)

# Criar conta
account = Account(
    account_number=AccountNumber(1),
    agency_number=AgencyNumber(1),
    client=client
)

# Realizar transações
from decimal import Decimal
from src.entities import Deposit, Withdraw

# Depósito (com logging automático via decorador)
deposit = Deposit(account, Decimal('1000.00'))
deposit.execute()

# Saque (com logging automático via decorador)
withdraw = Withdraw(account, Decimal('500.00'))
withdraw.execute()

## 🎯 Benefícios da Refatoração

1. **Manutenibilidade**: Código mais organizado e fácil de manter
2. **Extensibilidade**: Fácil adição de novos tipos de transação
3. **Testabilidade**: Cada componente pode ser testado isoladamente
4. **Legibilidade**: Código mais claro e auto-documentado
5. **Reutilização**: Componentes podem ser reutilizados em outros contextos
6. **Rastreabilidade**: Logging completo de todas as transações com timestamps

## 🔍 Decorador de Transações

O sistema implementa um decorador `@transaction_logger` que é aplicado automaticamente a todos os métodos `execute()` das transações bancárias.

### Funcionalidades do Decorador

- **📅 Registro de Timestamp**: Cada transação armazena sua data/hora de início
- **⏱️ Medição de Duração**: Calcula o tempo de execução de cada transação
- **📊 Informações Detalhadas**: Exibe dados da conta, cliente e valores
- **✅ Status de Execução**: Indica se a transação foi bem-sucedida ou falhou
- **🚨 Tratamento de Erros**: Captura e exibe erros durante a execução

### Exemplo de Saída do Decorador

```
============================================================
🕐 INÍCIO DA TRANSAÇÃO: Deposit
📅 Data/Hora: 31/08/2025 às 14:30:38
💰 Valor: R$ 1000.00
🏦 Conta: 00000001
👤 Cliente: João Silva
============================================================

============================================================
✅ TRANSAÇÃO CONCLUÍDA: Deposit
📅 Data/Hora: 31/08/2025 às 14:30:40
⏱️  Duração: 2.00 segundos
🎯 Status: Sucesso
============================================================
```

---

## 👤 Autor

**Bruno Batista**

📧 Email: brunojbatista@hotmail.com  
📱 Telefone: +55 (81) 9 9929-0698 — WhatsApp / Telegram  
🔗 [LinkedIn](https://www.linkedin.com/in/bruno-batista/)

Projeto desenvolvido como desafio prático da [DIO](https://www.dio.me/).

### Histórico de Versões

- **v1.0**: Sistema bancário básico com classes Account e CheckingAccount
- **v2.0**: Implementação do padrão Strategy com classes Transaction, Deposit e Withdraw
- **v2.1**: Simplificação da hierarquia de classes e melhorias na arquitetura
- **v3.0**: Sistema de transações com lista de objetos e classe Transfer dedicada
- **v3.1**: Implementação de decorador para logging de transações com timestamp
