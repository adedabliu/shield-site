# Plano do blog da Shield (/conteudo/)

Objetivo: gerar tráfego orgânico com conteúdo **próprio** sobre crédito com garantia de imóvel,
consórcio e financiamento. Nada de reescrever notícias de terceiros (risco de "scaled content abuse"
no Google e de direito autoral).

## Arquitetura

- O blog mora em `/conteudo/` (já está no menu e no sitemap). Cada artigo vira `/conteudo/<slug>/`.
- Fonte dos artigos: `_blog/posts/AAAA-MM-DD-slug.md` (Markdown com cabeçalho de metadados).
- Gerador: `python3 _blog/build.py` (só biblioteca padrão do Python). Ele:
  - gera a página de cada artigo com o visual do site (cabeçalho, rodapé, fontes, CSS);
  - inclui schema `BlogPosting`, `BreadcrumbList` e `FAQPage` (quando o artigo tem perguntas);
  - regenera o índice `/conteudo/`, o feed `/conteudo/feed.xml` e o bloco do blog no `sitemap.xml`;
  - liga cada artigo à página do produto correspondente e ao simulador.
- Molde visual: `_blog/molde.html` (copiado do site publicado). Se o cabeçalho ou o rodapé do site
  mudarem, atualize o molde.
- Atenção: a branch `fonte` (gerador das páginas de produto) está desatualizada em relação à `main`
  (ex.: endereço sala 65 x 63, favicon, página de links). Não rode `build/build.py` sem antes
  sincronizar, senão desfaz correções feitas direto na `main`.

## Cadência (dias úteis)

| Dia | Formato | Tamanho |
|---|---|---|
| Seg, Qua, Sex | Artigo completo (guia, comparativo, caso anonimizado, simulação) | 700–1.200 (cauda longa) ou 1.200–2.000 (pilar) |
| Ter, Qui | Dúvida respondida (uma pergunta real, resposta direta e completa) | 500–800 palavras |

Qualidade acima de volume: se não houver pauta boa no dia, não publica.

## Fluxo diário (decisão D-012 do Segundo Cérebro, 20/11/2026)

1. A tarefa agendada roda a skill `pauteiro-seo-shield`.
2. A skill escolhe a pauta (dúvidas reais de clientes, demanda de busca, experiência da Shield,
   temas perenes), checa no `_blog/pautas.md` o que já saiu, faz o briefing e escreve com a
   `especialista-seo-shield`.
3. Salva o `.md`, roda o gerador, confere e abre um pull request no GitHub.
4. Um agente separado revisa com o `agente-shield` e o Segundo Cérebro (produto, compliance,
   números, decisões, LGPD) e devolve APROVADO ou REPROVADO.
5. Aprovado: merge automático, conferência da página no ar e registro no Diário de ações
   autônomas. Reprovado: uma correção e nova revisão; se reprovar de novo, o PR fica para o
   Andrew no Painel Souvrin AI.
6. O Andrew recebe um push com o link do que saiu (ou do que travou) e pode vetar: o veto
   reverte o merge e vira decisão nova.

## Regras de conteúdo

- Sem promessa de taxa, aprovação ou prazo de contemplação; números como referência, com ressalva.
- Sem citar nome de cliente; casos sempre anonimizados.
- Toda afirmação regulatória (lei, BCB, CMN) conferida na fonte oficial e linkada.
- Cada artigo tem: palavra-chave principal, uma resposta direta no primeiro parágrafo,
  link para a página do produto, chamada para o simulador e data de atualização.

## Etapas

- [x] 1. Registrar este plano
- [x] 2. Gerador do blog
- [x] 3. Três primeiros artigos (dívida cara, carta contemplada, LTV)
- [x] 4. Verificação e pull request
- [x] 5. Skill `pauteiro-seo-shield`
- [x] 6. Tarefa agendada diária (dias úteis, 6h34, abre PR)
