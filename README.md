# Laboratório de Test Smells - Gerenciador de Usuários

## Trabalho executado

A suíte original permanece em `test/userService.smelly.test.js`. A suíte refatorada está em `__tests__/userService.clean.test.js`, conforme o caminho pedido no enunciado. O serviço em `src/userService.js` foi preservado.

| Etapa | Execução e resultado |
| --- | --- |
| 1. Ambiente | Dependências instaladas; suíte inicial: 4 testes aprovados e 1 ignorado. O clone existente aponta para `https://github.com/Victorgabrielcruz/test-smelly`. |
| 2. Análise manual | Cinco problemas documentados em `docs/analise-manual.md`, com localização, risco e solução. |
| 3. ESLint | `.eslintrc.json` com regras recomendadas e regras do enunciado. ESLint 8.57.1 e plugin Jest 28.14.0 fixados para reproduzir a configuração legada exigida. |
| 4. Detecção | Primeira execução: 4 erros e 2 avisos. Saída real e JSON salvos em `docs/evidencias/`. |
| 5. Refatoração | 17 casos limpos com AAA, cenários separados, `toThrow` e verificações do conteúdo do relatório. |
| 6. Validação | Suíte limpa: 17 aprovados; suíte conjunta: 21 aprovados e 1 ignorado; lint limpo: 0 problemas; cobertura limpa: 100% em linhas, instruções, funções e branches. |

### Executar

```bash
npm ci
npm test -- --runInBand
npm run lint:clean
npm run coverage:clean
```

O projeto usa CommonJS (`require`/`module.exports`). O `type` do `package.json` foi alinhado ao código existente. O `package-lock.json` é versionado para fixar a instalação.

O ESLint 8 é uma versão legada, escolhida para executar a `.eslintrc.json` exatamente como solicitado no trabalho. Uma migração para versões atuais exige rever essa configuração; não é necessária para reproduzir este laboratório.

`npm run lint` analisa também a suíte original e termina com código 1, mantendo os 4 erros e 2 avisos deliberados. `npm run lint:clean` valida o serviço e a suíte nova e exige zero avisos. O único teste ignorado está no arquivo original, que não foi alterado.

Se o lançador `npm` desta máquina continuar com o caminho interno quebrado, execute os comandos pela instalação existente:

```powershell
& 'C:\Program Files\nodejs\node.exe' 'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js' test -- --runInBand
& 'C:\Program Files\nodejs\node.exe' 'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js' run lint:clean
```

### Evidências e relatório

- `docs/analise-manual.md`: diagnóstico e comparação com a ferramenta.
- `docs/evidencias/`: logs reais, resultados JSON, códigos de saída e imagem da saída inicial do ESLint.
- `output/pdf/relatorio-test-smells.pdf`: relatório de quatro páginas; a identificação acadêmica depende de `docs/identificacao.json`.
- `scripts/gerar_relatorio.py`: fonte editável do relatório. Requer Python com ReportLab e Pillow.

```bash
node scripts/coletar-evidencias.cjs final
node scripts/validar-regressoes.cjs
python scripts/gerar_relatorio.py
```

`coletar-evidencias.cjs inicial` e `deteccao` registram a linha de base e devem ser usados antes de criar a suíte limpa. Os registros iniciais entregues foram produzidos nessa ordem. O coletor chama os executáveis locais do Jest/ESLint por Node; os logs identificam o comando npm equivalente e os arquivos `.execucao.json` registram os argumentos e códigos reais.

As verificações de regressão usam somente cópias temporárias em `tmp/`: ao remover a validação de idade, a suíte original passa e a limpa falha; ao alterar a apresentação do relatório mantendo os dados, a original falha e a limpa passa. Esses dois experimentos demonstram melhorias específicas e não constituem uma campanha completa de testes de mutação.

Antes de entregar, informe nome completo e matrícula em `docs/identificacao.json` e regenere o PDF. A disciplina usada na capa foi inferida do README original e pode ser ajustada nesse mesmo arquivo.

Este repositório serve como base para o trabalho prático sobre **Test Smells** na disciplina de Teste de Software. Ele contém uma suíte de testes que, apesar de passar, está repleta de "maus cheiros" (smells) que comprometem sua qualidade, manutenibilidade e eficácia.

## Contexto do Projeto

Imagine que você foi contratado(a) como Engenheiro(a) de Qualidade de Software em uma equipe que está desenvolvendo um serviço de gerenciamento de usuários (`UserService`).

A suíte de testes em `test/userService.smelly.test.js` foi escrita por um desenvolvedor que se concentrou apenas em fazer os testes passarem, sem se preocupar com boas práticas. O resultado é um código de teste frágil, obscuro e difícil de manter.

Sua missão é analisar, diagnosticar e refatorar essa suíte de testes, transformando-a em um exemplo de código de teste limpo e robusto.

## Sua Missão

Seu trabalho será dividido em três etapas principais:

1.  **Analisar:** Identificar manualmente e com a ajuda de ferramentas de análise estática (ESLint) os diferentes Test Smells presentes no código.
2.  **Refatorar:** Reescrever os testes em um novo arquivo (`userService.clean.test.js`), corrigindo os problemas encontrados e aplicando as melhores práticas, como o padrão **Arrange, Act, Assert (AAA)**.
3.  **Validar:** Provar que a refatoração foi bem-sucedida, garantindo que os novos testes passem, estejam livres de avisos do linter e sejam mais claros e eficazes.

## Como Começar (Setup)

Siga os passos abaixo para preparar seu ambiente de trabalho.

**1. Clone o repositório:**

```bash
git clone [URL_DO_SEU_FORK_DO_REPOSITORIO]
cd test-smelly
```
