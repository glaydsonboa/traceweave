# Guia: como criar um servidor MCP

Este guia usa o `traceweave-mcp` (`traceweave/mcp_server.py`) como exemplo trabalhado. Cada
regra abaixo existe porque, sem ela, o servidor falhou ou ficou inseguro durante a construção dele.

## 1. O que é um servidor MCP

Um servidor MCP (Model Context Protocol) é um processo que oferece a um agente três tipos de coisa:

| tipo | serve para | exemplo no traceweave |
|---|---|---|
| **tool** | uma ação que o agente chama com argumentos | `traceweave_write_text(path, content)` |
| **resource** | um dado que o agente lê por URI | `traceweave://status` |
| **prompt** | um modelo de instrução reutilizável | (não usado) |

O agente escolhe os argumentos. **Todo argumento de tool deve ser tratado como entrada não confiável**,
mesmo que o agente seja o seu.

## 2. Decida antes de escrever código

1. **Escopos.** Separe o que só lê, o que altera o disco e o que publica para fora da máquina. Cada
   grupo vira um escopo que precisa ser ligado explicitamente. O padrão é o mais fraco.
2. **Raiz.** Defina de qual diretório o servidor pode tocar e recuse todo o resto.
3. **Transporte.** Use `stdio` para uso local. `streamable-http` é para rede, e nunca deve ser
   exposto sem autenticação (veja a seção 10).
4. **Destino externo.** Se o servidor publica em algum lugar, trave esse lugar na configuração.
   Não confie no que o agente pedir.

## 3. Esqueleto mínimo

```python
from mcp.server import MCPServer

mcp = MCPServer("MeuServidor")

@mcp.tool()
def minha_tool(argumento: str) -> dict:
    """A docstring é a descrição que o agente lê. Seja preciso sobre o que a tool faz."""
    return {"ok": True}

def main() -> int:
    mcp.run()          # stdio
    return 0
```

No `pyproject.toml`, declare a dependência e um comando:

```toml
dependencies = ["mcp>=2,<3"]

[project.scripts]
meu-mcp = "meu_pacote.mcp_server:main"
```

**Declare também tudo o que o código precisa para importar.** No traceweave, `tzdata` faltava, e
no Windows o módulo `v2.provenance` não chegava a carregar.

## 4. Autorização por escopo

```python
def _scopes() -> set[str]:
    raw = os.environ.get("MEU_MCP_SCOPES", "read")        # padrão: o mais fraco
    return {s.strip().lower() for s in raw.split(",") if s.strip()}

def _require(scope: str) -> None:
    if scope not in _scopes():
        raise PermissionError(f"escopo {scope!r} não autorizado")
```

A primeira linha de toda tool chama `_require`. O escopo vem do ambiente do processo, nunca de um
argumento da tool.

## 5. Fronteira de caminho

```python
def _safe_path(rel: str) -> Path:
    root = _root()
    candidate = (root / rel).resolve()
    candidate.relative_to(root)                    # ValueError se escapar da raiz
    if candidate == root / ".git" or (root / ".git") in candidate.parents:
        raise ValueError("acesso a .git proibido")
    return candidate
```

Isso impede `../`, caminhos absolutos e escrita direta dentro de `.git`.

## 6. Nunca deixe um argumento virar opção de comando

**É o erro mais perigoso, e passa fácil em revisão.** Quando a tool repassa um argumento a um
programa como `git`, um valor que comece com `-` é lido como **opção**, e não como dado.

| argumento | valor malicioso | efeito |
|---|---|---|
| `ref` numa leitura | `--output=arquivo` | uma tool de leitura escreve em disco |
| `query` numa busca | `--open-files-in-pager=comando` | uma tool de leitura executa comando |
| `remote` num push | `--receive-pack=comando` | executa comando no push |

Correções, em ordem de preferência:

1. Use o marcador do próprio programa: `grep -e <padrão>`, `rev-parse --end-of-options <ref>`, e
   `--` antes de caminhos.
2. Recuse valores que comecem com `-`:

   ```python
   def _reject_option(value: str, name: str) -> str:
       if not value or value.lstrip().startswith("-"):
           raise ValueError(f"{name} inválido: {value!r}")
       return value
   ```

3. Para destinos (remote, URL, bucket), aceite só nomes configurados, e trave o destino com uma
   variável como `TRACEWEAVE_ALLOWED_REMOTE=dono/repositorio`.

Nunca use `shell=True`. Sempre passe uma lista de argumentos.

## 7. Escrita segura

- **Atômica:** grave num arquivo temporário e troque com `os.replace`. Assim o leitor nunca vê um
  arquivo pela metade.
- **Otimista:** aceite `expected_sha256`. Se o arquivo mudou desde que o agente o leu, recuse. Isso
  impede sobrescrever o trabalho de outro agente com um estado antigo.
- **Devolva prova:** o SHA-256 antes e depois, e o número de bytes.

## 8. Publicação

- Faça o stage **só** dos caminhos que o agente listou. Nunca use `git add .` ou `-A`.
- Recuse o commit se outro processo já tiver deixado coisa no stage.
- Push sem `--force`, só para o branch atual.
- **Confira o resultado no destino:** depois do push, leia o SHA remoto e compare com o local. Uma
  publicação só conta como feita com `readback_match: true`.
- Não rejeite conteúdo literal. O `git diff --cached --check` recusa espaço no fim de linha, e em
  transcripts e falas citadas esse espaço é conteúdo.

## 9. Testes

Escreva **um teste para cada porta fechada**, criando um repositório temporário no `setUp`:

```python
def test_readback_rejeita_ref_com_cara_de_opcao(self):
    with self.assertRaises(ValueError):
        mcp_server.traceweave_git_readback("--output=pwned.txt", "README.md")
    self.assertFalse((self.root / "pwned.txt").exists())   # prova o efeito, não só o erro
```

Cada teste precisa mostrar que o efeito perigoso **não aconteceu**, e não apenas que houve uma
exceção. Declare o executor de testes (`pytest` no extra `[test]`) para que quem clona consiga rodar.

## 10. Rede

`streamable-http` sem autenticação expõe as tools a qualquer um que alcance a porta. Para acesso
remoto, coloque o servidor atrás de OAuth 2.1 compatível com MCP e de TLS. Os escopos são autorização
de **processo**. Eles não substituem a autenticação de **rede**.

## 11. Conectar no Claude Code

```bash
claude mcp add meu-mcp --scope user \
  -e MEU_MCP_ROOT="C:\caminho" \
  -e MEU_MCP_SCOPES=read \
  -- "C:\caminho\.venv\Scripts\meu-mcp.exe"

claude mcp get meu-mcp          # deve mostrar ✔ Connected
```

O que aprendemos na prática:

- **Uma sessão aberta não enxerga um servidor recém-adicionado.** Rode `/mcp` para reconectar, ou
  reinicie com `claude -c`. Um erro de outro conector no `/mcp` não impede o seu de conectar.
- **Mudar uma variável de ambiente exige remover e adicionar de novo** (`claude mcp remove` e
  `claude mcp add`).
- **Se o servidor faz commit, dê a ele uma identidade** (`GIT_AUTHOR_NAME`/`EMAIL`,
  `GIT_COMMITTER_*`). Sem ela, o `git commit` falha numa máquina sem configuração global.
- Comece só com `read`. Libere `write` e `publish` depois que os testes de segurança passarem.

## 12. Checklist antes de liberar

- [ ] O escopo padrão é só leitura, e cada tool chama `_require` na primeira linha.
- [ ] Todo caminho passa por `_safe_path`, e `.git` está bloqueado.
- [ ] Nenhum argumento vira opção: `-e`, `--end-of-options`, `--` e recusa de `-`.
- [ ] O destino de publicação está travado na configuração.
- [ ] A escrita é atômica e tem `expected_sha256`.
- [ ] A publicação confere o resultado no destino.
- [ ] Há um teste por porta fechada, provando que o efeito não aconteceu.
- [ ] Todas as dependências, inclusive as de teste, estão declaradas.
- [ ] O servidor aparece como `✔ Connected`, e uma chamada real devolveu o resultado esperado.
