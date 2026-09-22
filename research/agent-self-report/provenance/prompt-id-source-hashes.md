# Fontes e versões

## Transcript principal

- Session ID: `2ed6e0a9-36fa-4eb3-9290-ebb3d226d30d`
- SHA-256 do arquivo recebido: `2828573ce955b96aadb3b534b893c9f7170c9232eed79c97056697b7fe3245b0`
- bytes: `109950`
- incluído no ZIP: apenas excerpt + hash

## Transcript de corroboração

- Session ID: `cb7bfd6a-a856-4a27-8b6e-ed6f2a038682`
- SHA-256 do arquivo recebido: `1653fc538cb1949b125b1c043ef8e04fd5bf1e9ad118f1f782d9573508b109eb`
- bytes: `3296`
- incluído no ZIP: apenas excerpt + hash

## Fonte histórica do gerador de cadeia

Fonte consultada: `leedermix-arch/worion-desktop`, ref `canonical/worion`, path histórico `scripts/generate-prompt-id.js`.

- Git blob SHA-1 histórico: `a3a9d374ddbbdae155133c8c704802ead956a5fe`
- bytes históricos: `5731`
- SHA-256 da cópia histórica: `b6c6f4188973e2b9032b3c6e1e739137df056c509e8e959966f0b113e830dc2f`

O código público atual NÃO é byte a byte essa fonte histórica. Ele é uma derivação neutra publicada em:

`research/agent-self-report/source-artifacts/identity-chain-generator.js`

Alterações deliberadas da derivação pública:
- remove nomes e contratos específicos do sistema de origem;
- troca os prefixos por `PROV-CMD / PROV-PROMPT / PROV-EXEC / PROV-RESP / PROV-ART / PROV-EVT`;
- renomeia a API para `generateId`;
- resolve a raiz real do repositório com `git rev-parse --show-toplevel` antes do `git grep`, evitando que o caminho abstrato limite a busca à subpasta;
- preserva formato temporal, sanitização, operação local e sem rede.

SHA-256 da derivação pública validada antes da publicação:
`8338e9dc115f2fda1271b0512bb0a7b889cd7d9a92ff8265accad548bace9c00`

Validação local antes da publicação:
- `node --check`: PASS
- geração `prompt`: PASS
- geração `command`: PASS
- sanitização de slug acentuado: PASS

## Fonte histórica do gerador de par

Fonte: arquivo standalone mais recente disponível no acervo do projeto.

- bytes: `3237`
- SHA-256: `f2f966e9209fbd56d95fe2cffaa2f43fa7a9846329d975e2613ecec9a6f61d17`

A publicação desse segundo artefato permanece, nesta causa, como fonte histórica sob nome abstrato; não foi modificada por esta correção.
