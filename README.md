
# 💰 Sistema Bancário em Python

Projeto de um sistema bancário orientado a objetos, que permite ao usuário criar contas, realizar operações como depósito, saque, transferências entre contas e visualizar extratos.

## 📂 Estrutura

- `index.py`: Arquivo principal que inicia a execução do sistema.
- `Bank.py`: Gerencia clientes e suas contas bancárias.
- `Account.py`: Classe base para contas com funcionalidades de saldo, saque e depósito.
- `CheckingAccount.py`: Subclasse especializada para conta corrente.
- `Client.py`: Define o cliente com nome e CPF.
- `Utils.py`: Utilidades como validação de CPF, arredondamento de valores e limpeza do terminal.

## 🚀 Como Executar

1. Certifique-se de que o Python 3.8+ está instalado.
2. Navegue até a pasta onde os arquivos foram extraídos.
3. Execute o sistema com:

```bash
python index.py
```

## 🧠 Funcionalidades

- Cadastro de cliente com CPF
- Criação de conta corrente
- Login via CPF
- Depósito e saque com validações
- Transferência entre contas
- Extrato detalhado com timestamp

## ✅ Regras de Negócio

- CPF deve estar no formato válido `000.000.000-00`
- Saque máximo: R$500 por operação
- Até 3 saques por sessão
- Não é permitido transferir para si mesmo

---

## 👤 Autor

Projeto desenvolvido como desafio prático da [DIO](https://www.dio.me/).
