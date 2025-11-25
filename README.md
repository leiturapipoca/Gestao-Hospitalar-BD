# Gestao-Hospitalar-BD
Trabalho de Banco de Dados

# [FAQ]:

# [ITEM 1: Arquivo contendo as variáveis de ambiente não foi encontrado]:
O erro em questão indica que, dentro do diretório no qual se executou o programa (pwd/cwd), não foi encontrado o arquivo contendo as variáveis de ambiente.
Para corrigir o problema, basta criar, dentro do PWD, um arquivo de nome ".env.json" contendo as credenciais que devem ser utilizadas para acessar o banco de dados local.

Segue abaixo um exemplo da estrutura do arquivo ".env.json":
```json
{
	"host": "localhost",
	"database": "hosp",
	"user": "<nome do usuário do banco de dados>",
	"password": "<senha do usuário do banco de dados>"
}
```
