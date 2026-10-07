const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const output = path.join(root, 'docs', 'evidencias');
fs.mkdirSync(output, { recursive: true });

const mode = process.argv[2];
const commands = {
  inicial: [
    ['testes-iniciais', 'npm test -- --runInBand', 'jest/bin/jest.js',
      ['--runInBand', '--json', '--outputFile=docs/evidencias/testes-iniciais.json'], 0],
  ],
  deteccao: [
    ['eslint-inicial', 'npx eslint .', 'eslint/bin/eslint.js', ['.'], 1],
    ['eslint-inicial-json', 'npx eslint . --format json', 'eslint/bin/eslint.js',
      ['.', '--format', 'json', '--output-file', 'docs/evidencias/eslint-inicial.json'], 1],
  ],
  final: [
    ['eslint-final', 'npm run lint:clean', 'eslint/bin/eslint.js',
      ['src/', '__tests__/userService.clean.test.js', '--max-warnings=0'], 0],
    ['testes-finais', 'npm test -- --runInBand', 'jest/bin/jest.js',
      ['--runInBand', '--json', '--outputFile=docs/evidencias/testes-finais.json'], 0],
    ['cobertura-clean', 'npm run coverage:clean', 'jest/bin/jest.js',
      ['__tests__/userService.clean.test.js', '--runInBand', '--coverage',
        '--collectCoverageFrom=src/userService.js', '--coverageDirectory=coverage/clean'], 0],
    ['eslint-completo-final', 'npx eslint .', 'eslint/bin/eslint.js', ['.'], 1],
  ],
};

if (!commands[mode]) {
  console.error('Uso: node scripts/coletar-evidencias.cjs inicial|deteccao|final');
  process.exit(2);
}

for (const [name, display, binary, args, expected] of commands[mode]) {
  const executable = path.join(root, 'node_modules', binary);
  const result = spawnSync(process.execPath, [executable, ...args], {
    cwd: root,
    encoding: 'utf8',
    env: { ...process.env, FORCE_COLOR: '0' },
  });
  const text = `$ ${display}\n${result.stdout || ''}${result.stderr || ''}`;
  fs.writeFileSync(path.join(output, `${name}.txt`), text);
  fs.writeFileSync(path.join(output, `${name}.execucao.json`), JSON.stringify({
    comandoEquivalente: display,
    executavel: 'node',
    argumentos: [path.relative(root, executable).replaceAll('\\', '/'), ...args],
    codigoSaida: result.status,
    codigoEsperado: expected,
    erroExecucao: result.error?.message || null,
  }, null, 2) + '\n');
  process.stdout.write(text);
  if (result.status !== expected) {
    console.error(`Código inesperado em ${name}: ${result.status}; esperado: ${expected}.`);
    process.exit(1);
  }
}
