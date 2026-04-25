# Industria Alfa API

API de segurança industrial para execução controlada de comandos em equipamentos, com autenticação por perfil e bloqueio de entradas maliciosas.

## Funcionalidades

- Autenticação Basic Auth com controle de perfis (`admin` / `operator`)
- Validação e bloqueio de comandos maliciosos
- Endpoint de health check
- Configuração 100% por variáveis de ambiente — sem credenciais no código

## Rotas

| Método | Rota               | Autenticação | Descrição                        |
|--------|--------------------|--------------|----------------------------------|
| GET    | `/health`          | Não          | Verifica se o servidor está ativo |
| POST   | `/execute-command` | Sim (admin)  | Executa um comando no equipamento |

### POST `/execute-command`

**Body:**
```json
{
  "command": "REBOOT"
}
```

**Comandos permitidos:** `REBOOT`, `CALIBRATE`, `STATUS_CHECK`

**Resposta de sucesso (200):**
```json
{
  "status": "Executado",
  "command": "REBOOT"
}
```

## Instalação local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/industria-alfa-api.git
cd industria-alfa-api
```

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com seus usuários e senhas. **Nunca envie o `.env` ao GitHub.**

### 4. Inicie o servidor

```bash
python main.py
```

O servidor sobe em `http://localhost:8080`.

## Exemplos de uso com curl

**Health check:**
```bash
curl http://localhost:8080/health
```

**Executar comando (como admin):**
```bash
curl -X POST http://localhost:8080/execute-command \
  -H "Authorization: Basic $(echo -n 'gestor:sua-senha' | base64)" \
  -H "Content-Type: application/json" \
  -d '{"command": "STATUS_CHECK"}'
```

## Deploy no Render

1. Suba o repositório no GitHub
2. Crie um novo **Web Service** no [Render](https://render.com)
3. Conecte ao repositório
4. Defina as variáveis de ambiente no painel do Render (aba **Environment**):
   - `API_USERS` — JSON com os usuários (veja `.env.example`)
   - `PORT` — o Render define automaticamente
5. O Render detecta o `requirements.txt` e instala as dependências automaticamente

## Perfis de acesso

| Role       | read_sensor | send_command | update_firmware |
|------------|-------------|--------------|-----------------|
| `admin`    | ✓           | ✓            | ✓               |
| `operator` | ✓           | ✗            | ✗               |

## Estrutura do projeto

```
industria-alfa-api/
├── main.py          # Ponto de entrada
├── config.py        # Leitura de variáveis de ambiente
├── handlers.py      # Lógica dos endpoints HTTP
├── security.py      # Autenticação e validação de comandos
├── requirements.txt # Dependências Python
├── .env.example     # Template de configuração
├── .gitignore       # Arquivos ignorados pelo Git
├── LICENSE          # Licença MIT
└── README.md        # Esta documentação
```

## Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature: `git checkout -b minha-feature`
3. Faça commit das mudanças: `git commit -m 'feat: minha feature'`
4. Abra um Pull Request descrevendo o que foi feito

## Licença

MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.