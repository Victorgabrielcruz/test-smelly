# Etapa 2 - Análise manual dos Test Smells

Arquivo analisado: `test/userService.smelly.test.js`. A análise foi realizada antes da refatoração. O arquivo original será preservado integralmente para comparação.

| Smell | Localização original | Problema e risco | Refatoração prevista |
| --- | --- | --- | --- |
| Eager Test | Teste "deve criar e buscar um usuário corretamente", linhas 18-31 | Mistura criação e busca, com duas ações intercaladas com verificações. Uma falha dificulta identificar qual contrato foi violado. | Separar criação de busca e aplicar Arrange, Act, Assert (AAA) em cada cenário. |
| Conditional Test Logic | Teste de desativação, linhas 33-52 | O `for` executa diferentes cenários; o `if/else` decide quais expectativas executar. O leitor precisa interpretar o fluxo e a verificação depende dos próprios dados do usuário. | Criar casos independentes para usuário comum, administrador e ID inexistente, sem condicionais. |
| Fragile Test | Teste de relatório, linhas 54-64 | Exige uma linha com pontuação, ordem, espaços e quebra de linha exatos. Alterações de apresentação podem quebrar o teste sem alterar as informações relevantes. | Verificar os dados relevantes do relatório sem exigir uma linha inteira com formatação exata. |
| Verificação condicional de exceção / falso positivo | Teste de menor de idade, linhas 66-74 | O `expect` está somente no `catch`. Se a validação for removida, nenhuma expectativa será executada e o teste passará. | Usar `expect(acao).toThrow(mensagem)`, que exige que a exceção realmente ocorra. |
| Disabled Test | Teste com `test.skip`, linhas 77-79 | O cenário de ausência de usuários não é executado e seu corpo está vazio. O nome fala em "lista", embora a API retorne um relatório textual. | Implementar um teste ativo para a mensagem de ausência de usuários no relatório. |

## Observações sobre a ferramenta

O ESLint identifica expectativas condicionais e testes ignorados pelas regras do plugin Jest. Não se deve atribuir a ele a identificação automática de todos os smells: Eager Test e fragilidade semântica do relatório exigem revisão manual nesta configuração. Não há recurso externo oculto na suíte; por isso, não foi classificado um "Convidado Misterioso" apenas por existir um objeto de dados compartilhado.

O `beforeEach` já cria o serviço e limpa o banco em memória. Esse isolamento será mantido. O uso de `_clearDB()` é uma dependência da API auxiliar existente; a proposta é refatorar os testes sem alterar as regras de negócio.
