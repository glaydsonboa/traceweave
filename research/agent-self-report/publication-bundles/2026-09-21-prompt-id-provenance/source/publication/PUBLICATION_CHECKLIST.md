# Checklist de autorização/publicação

STATUS ATUAL: PRE_PUBLICATION — NÃO PUBLICADO

Antes de publicar:

- [ ] Glaydson leu e autorizou o conteúdo.
- [ ] Confirmar se o caso será publicado como `PROVENANCE_GAP` e não como "execução falsa".
- [ ] Se existir JSONL nativo da sessão, confrontar o evento antes de elevar a conclusão.
- [ ] Executar `generate-update-ids.js <slug>` apenas quando a atualização pública for realmente iniciar.
- [ ] Preservar `NOTION_ID`, `GITHUB_ID` e `PAIR_KEY` sem regenerar durante a mesma atualização.
- [ ] Publicar no GitHub somente o conjunto autorizado.
- [ ] Registrar SHA/Issue/commit/release nativo e fazer readback.
- [ ] Publicar no Notion somente se autorizado.
- [ ] Registrar page_id nativo e fazer readback.
- [ ] Atualizar `PUBLICATION_PROOF_TEMPLATE.json` com fatos reais.
- [ ] Se Git fizer parte do fechamento: commit → push → readback → local HEAD == remote HEAD.
- [ ] STOP só pode ser `COMPLETE` se os campos obrigatórios dessa publicação estiverem verificados.
- [ ] Não incluir transcript integral sem revisão específica de PII/segredos.

## Sanitização desta pré-publicação

O ZIP não contém os transcripts integrais.

Ele contém:
- hashes dos originais recebidos;
- excerpts necessários;
- nenhum token detectado nos excerpts selecionados;
- nenhum valor de segredo copiado dos arquivos de origem;
- geradores sem credenciais.

Isso reduz a superfície de exposição antes da autorização final.
