
# 💰 Sistema Bancário em Python

Este é um projeto de sistema bancário em Python, desenvolvido como desafio prático. O sistema permite a criação e autenticação de contas bancárias, com suporte para operações como **depósito**, **saque**, **transferência** e **visualização de extrato**.

## 🧩 Estrutura do Projeto

- `index.py`: Arquivo principal, ponto de entrada do sistema (executar este arquivo para iniciar o sistema).
- `Bank.py`: Contém a classe `Bank`, que gerencia múltiplas contas e autenticação.
- `Account.py`: Implementa a estrutura e regras de uma conta bancária.
- `CheckingAccount.py`: Herda de `Account`, especializada em conta corrente.
- `Client.py`: Representa o cliente, contendo CPF e nome.
- `Utils.py`: Funções auxiliares como validação de CPF, arredondamento e limpeza de terminal.

## 🚀 Como Executar

1. Certifique-se de ter o Python 3.8+ instalado.
2. Clone o repositório ou extraia os arquivos.
3. No terminal, execute o comando:

```bash
python index.py
```

4. Siga as instruções do menu para:

- Criar uma conta
- Logar com CPF
- Realizar operações (depósito, saque, extrato, transferência)
- Encerrar sessão

## ⚠️ Validações e Regras de Negócio

- **CPF:** Deve ser válido (formato `000.000.000-00`) para criar ou acessar conta.
- **Depósito:** Não são aceitos valores negativos ou zero.
- **Saque:** 
  - Máximo de R$500,00 por operação.
  - Limite de até 3 saques por sessão.
  - Verifica saldo disponível.
- **Transferência:** Não permite transferir para a própria conta. Verifica CPF de destino.

## 📦 Exemplo de Execução

```bash
Bem vindo!
Escolha uma opção:

[c] Criar Conta
[l] Logar com CPF
[q] Sair

=> c
Informe seu nome: João
Informe seu CPF (formato 000.000.000-00): 123.456.789-00
Conta criada com sucesso!
```

## ✅ Funcionalidades Implementadas

- [x] Cadastro de cliente com CPF
- [x] Criação de conta corrente
- [x] Login via CPF
- [x] Depósito e saque com regras
- [x] Transferência entre contas
- [x] Extrato com timestamp
- [x] Validações robustas

## 📁 Organização de Código

O projeto utiliza orientação a objetos com separação clara de responsabilidades:

- Cliente (`Client`)
- Conta bancária (`Account`, `CheckingAccount`)
- Gerenciador de contas e autenticação (`Bank`)
- Utilitários (`Utils`)

---

## 🧑‍💻 Autor

Este projeto foi desenvolvido como parte do desafio da [DIO.me](https://www.dio.me/).  
Sinta-se livre para usar, modificar e expandir.
