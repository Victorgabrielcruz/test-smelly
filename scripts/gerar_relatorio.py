"""Gera o relatório de quatro páginas a partir das evidências locais."""
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
EVIDENCES = ROOT / 'docs' / 'evidencias'
OUTPUT = ROOT / 'output' / 'pdf' / 'relatorio-test-smells.pdf'
IDENTITY = json.loads((ROOT / 'docs' / 'identificacao.json').read_text(encoding='utf-8'))

FONT_DIR = Path('C:/Windows/Fonts')
if (FONT_DIR / 'arial.ttf').exists():
    pdfmetrics.registerFont(TTFont('ReportSans', str(FONT_DIR / 'arial.ttf')))
    pdfmetrics.registerFont(TTFont('ReportSansBold', str(FONT_DIR / 'arialbd.ttf')))
    pdfmetrics.registerFontFamily('ReportSans', normal='ReportSans', bold='ReportSansBold')
    pdfmetrics.registerFont(TTFont('ReportMono', str(FONT_DIR / 'consola.ttf')))
    SANS, BOLD, MONO = 'ReportSans', 'ReportSansBold', 'ReportMono'
else:
    SANS, BOLD, MONO = 'Helvetica', 'Helvetica-Bold', 'Courier'

NAVY = colors.HexColor('#173047')
TEAL = colors.HexColor('#087F8C')
MUTED = colors.HexColor('#526476')
LIGHT = colors.HexColor('#EDF3F7')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle('TitleReport', fontName=BOLD, fontSize=25, leading=31,
                          textColor=NAVY, spaceAfter=22))
styles.add(ParagraphStyle('HeadingReport', fontName=BOLD, fontSize=17, leading=22,
                          textColor=NAVY, spaceAfter=16))
styles.add(ParagraphStyle('SubReport', fontName=BOLD, fontSize=11.5, leading=15,
                          textColor=TEAL, spaceBefore=13, spaceAfter=5))
styles.add(ParagraphStyle('BodyReport', fontName=SANS, fontSize=10, leading=14,
                          textColor=NAVY, spaceAfter=8))
styles.add(ParagraphStyle('SmallReport', fontName=SANS, fontSize=8.3, leading=11.5,
                          textColor=MUTED, spaceAfter=7))
styles.add(ParagraphStyle('CodeReport', fontName=MONO, fontSize=8.2, leading=11,
                          textColor=NAVY, backColor=LIGHT, borderPadding=10,
                          spaceBefore=4, spaceAfter=12))
styles.add(ParagraphStyle('LabelReport', fontName=BOLD, fontSize=9, leading=13,
                          textColor=TEAL, spaceAfter=13))

story = []


def paragraph(text, style='BodyReport'):
    story.append(Paragraph(text, styles[style]))


def heading(text):
    paragraph(text, 'SubReport')


def summary_table(rows, widths=(230, 265)):
    cells = [[Paragraph(escape(str(cell)), styles['BodyReport']) for cell in row]
             for row in rows]
    table = Table(cells, colWidths=widths, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#D3DDE5')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(table)


def code(text):
    story.append(Preformatted(text.rstrip(), styles['CodeReport']))


def footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor('#D3DDE5'))
    canvas.line(48, 36, width - 48, 36)
    canvas.setFont(SANS, 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(48, 23, 'Teste de Software | Refatoração e Test Smells')
    canvas.drawRightString(width - 48, 23, f'{doc.page} / 4')
    if doc.page > 1:
        canvas.setFont(SANS, 7.5)
        canvas.drawString(48, height - 28, 'RELATÓRIO TÉCNICO')
        canvas.drawRightString(width - 48, height - 28, IDENTITY['data'])
    canvas.restoreState()


# Página 1: capa e síntese.
story.append(Spacer(1, 52))
paragraph(escape(IDENTITY['disciplina'].upper()), 'LabelReport')
paragraph('Refatoração de Testes<br/>e Detecção de<br/>Test Smells', 'TitleReport')
paragraph('Serviço de gerenciamento de usuários - UserService')
story.append(Spacer(1, 22))
paragraph('<b>Nome completo:</b> ' + escape(IDENTITY.get('nomeCompleto') or 'Pendente de informação'))
paragraph('<b>Matrícula:</b> ' + escape(IDENTITY.get('matricula') or 'Pendente de informação'))
paragraph('<b>Disciplina:</b> ' + escape(IDENTITY['disciplina']))
paragraph('<b>Data:</b> ' + escape(IDENTITY['data']))
if not IDENTITY.get('nomeCompleto') or not IDENTITY.get('matricula'):
    paragraph('Versão técnica concluída. Preencher nome completo e matrícula antes da entrega.',
              'SmallReport')
story.append(Spacer(1, 21))
heading('Síntese da execução')
summary_table([
    ['Verificação', 'Resultado observado'],
    ['Suíte original', '4 aprovados; 1 ignorado'],
    ['ESLint inicial', '4 erros; 2 avisos'],
    ['Suíte limpa', '17 aprovados; nenhum ignorado'],
    ['Validação conjunta', '21 aprovados; 1 ignorado original'],
    ['ESLint da suíte limpa e serviço', '0 erros; 0 avisos'],
])
story.append(Spacer(1, 20))
paragraph('<b>Repositório configurado no clone</b>', 'SmallReport')
url = escape(IDENTITY['repositorio'])
paragraph(f'<link href="{url}" color="#087F8C">{url}</link>', 'SmallReport')
paragraph('Suíte entregue: __tests__/userService.clean.test.js. O arquivo original permanece '
          'em test/userService.smelly.test.js, conforme a estrutura real do clone.', 'SmallReport')
story.append(PageBreak())

# Página 2: análise manual, com exatamente três smells principais.
paragraph('1. Análise dos Test Smells', 'HeadingReport')
paragraph('A leitura manual foi realizada antes da refatoração. O diagnóstico abaixo considera '
          'a suíte original, preservada integralmente, e relaciona os problemas aos seus riscos.')
heading('1.1 Eager Test - criação e busca no mesmo cenário')
paragraph('O teste das linhas 18-31 cria um usuário, verifica seu ID, busca o cadastro e verifica '
          'nome e status. Há duas ações intercaladas com expectativas. A falha pode ocorrer em '
          'contratos diferentes, dificultando a localização do problema e a manutenção do teste. '
          'Na suíte limpa, a criação e a consulta têm casos independentes, com preparação, '
          'uma ação principal e verificações específicas.')
heading('1.2 Conditional Test Logic - desativação em for e if')
paragraph('Nas linhas 33-52, um laço percorre um usuário comum e um administrador. Um '
          'if/else escolhe quais expectativas executar. A leitura exige simular o fluxo; '
          'mudanças nos dados podem alterar as verificações executadas. A versão limpa '
          'separa usuário comum, administrador e ID inexistente. Também verifica que o '
          'usuário comum continua cadastrado e que o administrador permanece ativo.')
heading('1.3 Fragile Test - formatação exata do relatório')
paragraph('Nas linhas 54-64, a expectativa exige ID, nome e status em uma linha com ordem, '
          'vírgulas, espaços e quebra de linha exatos. Isso acopla o teste à apresentação: '
          'o relatório pode continuar correto e o teste falhar. A refatoração verifica os '
          'IDs e nomes dos usuários e os estados ativo e inativo, sem exigir a linha inteira '
          'ou o cabeçalho decorativo. Essa escolha pressupõe que o formato não é um contrato '
          'de integração externo, como sugere o comentário do serviço.')
heading('Problemas adicionais identificados')
paragraph('<b>Exceção verificada somente no catch (linhas 66-74):</b> se a validação de idade '
          'não lançar erro, nenhuma expectativa roda e o teste passa. Esse falso positivo '
          'foi corrigido com toThrow e é demonstrado na próxima página.')
paragraph('<b>Teste ignorado e vazio (linhas 77-79):</b> test.skip impede a execução e deixa '
          'o cenário sem proteção. O nome também menciona uma lista, embora a API produza texto. '
          'Foi implementado um caso ativo para a mensagem de ausência de usuários no relatório.')
heading('Isolamento e limites do escopo')
paragraph('O beforeEach instancia o serviço e usa _clearDB() para limpar o banco em memória. '
          'Esse mecanismo foi mantido. Não houve alteração em src/userService.js. O uso da API '
          'auxiliar de limpeza é uma dependência explícita do projeto; não caracteriza, por si '
          'só, um recurso externo oculto ou Convidado Misterioso.')
story.append(PageBreak())

# Página 3: antes/depois e evidência de eficácia.
paragraph('2. Processo de refatoração', 'HeadingReport')
paragraph('Foi escolhido o teste de menor de idade porque ele pode mascarar a ausência de '
          'uma regra de negócio. Os trechos abaixo reproduzem os testes; apenas os comentários '
          'explicativos do trecho original foram omitidos.')
heading('Antes - expectativa executada apenas se houver erro')
code("""test('deve falhar ao criar usuário menor de idade', () => {
  try {
    userService.createUser('Menor', 'menor@email.com', 17);
  } catch (e) {
    expect(e.message).toBe('O usuário deve ser maior de idade.');
  }
});""")
heading('Depois - verificação obrigatória da exceção, com AAA')
code("""test('deve rejeitar um usuário com 17 anos', () => {
  // Arrange
  const nome = 'Menor';
  const email = 'menor@teste.com';
  const idade = 17;

  // Act
  const criarUsuario = () => userService.createUser(nome, email, idade);

  // Assert
  expect(criarUsuario).toThrow('O usuário deve ser maior de idade.');
});""")
paragraph('A ação é representada por uma função, pois toThrow precisa executar a chamada '
          'dentro do matcher para observar a exceção. Se o serviço aceitar 17 anos, a '
          'expectativa falha. A mensagem também é verificada, distinguindo a validação '
          'de idade de outros erros. Não há try/catch nem expectativas condicionais.')
heading('Decisões aplicadas aos demais cenários')
paragraph('A criação foi separada da busca; a desativação ganhou casos independentes; o '
          'relatório passou a verificar informações relevantes; o cenário vazio foi ativado. '
          'Os campos obrigatórios usam test.each: cada linha gera um teste independente, '
          'com o mesmo comportamento esperado e sem if ou for no corpo do teste. O limite '
          'de 18 anos e a preservação dos cadastros também foram verificados.')
heading('Experimentos controlados em cópias temporárias')
summary_table([
    ['Mudança simulada', 'Suíte original / suíte limpa'],
    ['Remoção da validação de idade', 'Passa / falha: defeito detectado pela limpa'],
    ['Alteração visual do relatório', 'Falha / passa: dados continuam preservados'],
])
paragraph('Os experimentos não modificam o serviço real. Os resultados e saídas estão em '
          'docs/evidencias/regressoes.json. São duas verificações específicas, não uma '
          'campanha completa de testes de mutação.', 'SmallReport')
story.append(PageBreak())

# Página 4: captura, detecção automática, validação e conclusão.
paragraph('3. Ferramenta, validação e conclusão', 'HeadingReport')
paragraph('A configuração .eslintrc.json usa eslint:recommended, plugin:jest/recommended '
          'e as três regras solicitadas. ESLint 8.57.1 e eslint-plugin-jest 28.14.0 foram '
          'fixados para reproduzir o formato legado do enunciado. A suíte limpa também '
          'ativa jest/no-conditional-in-test.')
heading('Primeira execução - npx eslint .')
png = EVIDENCES / 'eslint-inicial.png'
if not png.exists():
    raise FileNotFoundError('Gere a captura docs/evidencias/eslint-inicial.png antes do PDF.')
from PIL import Image as PILImage
with PILImage.open(png) as picture:
    image_width, image_height = picture.size
story.append(Image(str(png), width=495, height=495 * image_height / image_width))
story.append(Spacer(1, 5))
paragraph('Figura 1 - Captura do log real da primeira execução, exibido em um visualizador '
          'HTML para legibilidade. O texto original é entregue em eslint-inicial.txt.', 'SmallReport')
paragraph('A regra no-conditional-expect apontou três expectativas no if/else de desativação '
          'e uma no catch. Os avisos no-disabled-tests e expect-expect apontaram o teste '
          'ignorado e sem expectativas. A ferramenta não identificou automaticamente '
          'Eager Test nem a fragilidade semântica do relatório; esses itens vieram da revisão manual.')
heading('Validação final')
paragraph('A suíte limpa passou com 17 testes e o lint terminou com código 0, sem erros nem '
          'avisos. A execução conjunta aprovou 21 testes, com um único teste ignorado na '
          'suíte original. A cobertura da suíte limpa foi de 100% em linhas, instruções, '
          'funções e branches. O lint global ainda retorna 4 erros e 2 avisos no original '
          'preservado, resultado esperado para a comparação antes/depois.')
heading('Conclusão')
paragraph('Testes pequenos, nomes descritivos, AAA e expectativas obrigatórias tornam as '
          'falhas mais fáceis de interpretar e reduzem manutenção sem valor funcional. '
          'A análise estática oferece feedback repetível; a revisão manual avalia o '
          'significado e a fragilidade das verificações. Cobertura indica execução de código, '
          'mas não prova a detecção de todos os defeitos. Os experimentos confirmam duas '
          'melhorias concretas da suíte refatorada.')
paragraph('<b>Referências:</b> enunciado do trabalho; '
          '<link href="https://github.com/jest-community/eslint-plugin-jest" color="#087F8C">'
          'documentação oficial do eslint-plugin-jest</link>; '
          '<link href="https://eslint.org/docs/v8.x/use/configure/" color="#087F8C">'
          'documentação oficial do ESLint 8</link>. Evidências locais: docs/evidencias/.', 'SmallReport')

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=48, leftMargin=48,
                        topMargin=46, bottomMargin=48,
                        title='Refatoração de Testes e Detecção de Test Smells',
                        author=IDENTITY.get('nomeCompleto') or '',
                        subject='Análise manual, ESLint, refatoração AAA e validação')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUTPUT)
