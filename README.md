# Raciocinio Algorítmico - Sistema Bancário
Segundo Trabalho Discente Efetivo

# Grupo - Incoêrencia Algorítmica
* Vinicius Marques
* Leonardo Matthew Knight
* ...

## Sobre o Projeto
Sistema bancário, em que existem o sistema separado para o gerente e para o cliente utilizado através de linhas de comando

Essa é uma lista dos recursos utilizados para fazer esse projeto
### 🛠 Construido utilizando
- sqlite3
- argparse

## Principais Funcionalidades
### Gerente
- [x] Cadastro de cliente
- [x] Busca no banco de dados por clientes
- [x] Alteração de senha de clientes

### Cliente
- [x] Saque
- [x] Depósito
- [x] Visualização de saldo
- [x] Simulação de Investimento

## Como executa-lo
Se você ter acesso a um terminal
```bash
cd sistema_bancario
```
```bash
python gerente.py <comando>
```
```bash
python cliente.py <comando>
```
Para uma lista de comandos do gerente
```bash
python gerente.py -h ou --help
```
Para uma lista de comandos do cliente
```bash
python cliente.py -h ou --help
```
## Status
<h4 align="center"> 
	🚧  Ainda está em construção...  🚧
</h4>

## Para fazer:
- [ ] Validação de Senha [Gerente]
- [X] ~~Depósito [Cliente]~~
- [X] ~~Simulação de Investimento [Cliente]~~
- [ ] Hash para as senhas [Base de Dados]
