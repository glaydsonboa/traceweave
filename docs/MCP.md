# Traceweave MCP — leitura, escrita e publicação

O Traceweave expõe um servidor MCP local-first para operar o próprio repositório sem transformar acesso ao Git em escrita irrestrita.

## Capacidades

As permissões são separadas:

- `read` — status, listagem, leitura de arquivos, busca, SHA-256 e Git readback.
- `write` — criar, substituir e acrescentar conteúdo em arquivos dentro do repositório.
- `publish` — stage de caminhos explícitos, commit e push sem force.

`publish` não é implícito em `write`.

## Instalação

```bash
python -m pip install -e .
```

O pacote instala o comando:

```bash
traceweave-mcp
```

## Autorização local

Defina a raiz e os scopes no ambiente do processo MCP.

Somente leitura:

```text
TRACEWEAVE_ROOT=/caminho/traceweave
TRACEWEAVE_MCP_SCOPES=read
```

Leitura + escrita local:

```text
TRACEWEAVE_ROOT=/caminho/traceweave
TRACEWEAVE_MCP_SCOPES=read,write
```

Leitura + escrita + commit/push:

```text
TRACEWEAVE_ROOT=/caminho/traceweave
TRACEWEAVE_MCP_SCOPES=read,write,publish
```

O default é `read`.

## Transporte

Local, via stdio:

```bash
traceweave-mcp
```

HTTP local:

```bash
traceweave-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Endpoint:

```text
http://127.0.0.1:8000/mcp
```

Não exponha esse modo diretamente à Internet. Para acesso remoto, coloque o servidor atrás de autenticação OAuth 2.1 compatível com MCP e TLS.

## Tools

### read

- `traceweave_status`
- `traceweave_list`
- `traceweave_read_text`
- `traceweave_search_text`
- `traceweave_sha256`
- `traceweave_git_readback`

### write

- `traceweave_write_text`
- `traceweave_append_text`

As duas operações aceitam `expected_sha256` para impedir sobrescrita baseada em estado antigo.

### publish

- `traceweave_git_commit`
- `traceweave_git_push`

O commit exige caminhos explícitos. O MCP não usa `git add .` nem `git add -A`. O push não aceita branch diferente da branch corrente e não usa `--force`.

## Resource

```text
traceweave://status
```

Expõe HEAD, branch, raiz e scopes autorizados.

## Fronteiras

O servidor:

- rejeita caminhos que escapem de `TRACEWEAVE_ROOT`;
- bloqueia acesso direto a `.git`;
- preserva a separação entre editar e publicar;
- usa stage exato;
- executa `git diff --cached --check` antes do commit;
- confirma o SHA remoto depois do push;
- não faz reset, amend, stash, force-push ou limpeza implícita.

A autenticação de rede não é substituída pelos scopes. Os scopes são autorização operacional do processo. Em implantação remota, autenticação HTTP deve ser adicionada na camada de deploy.
