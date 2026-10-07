const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'src/userService.js'), 'utf8');
const cases = [
  {
    name: 'validacao-idade-removida',
    before: "    if (idade < 18) {\n      throw new Error('O usuário deve ser maior de idade.');\n    }",
    after: '',
    expected: { smelly: 0, clean: 1 },
  },
  {
    name: 'apresentacao-relatorio-alterada',
    before: 'ID: ${user.id}, Nome: ${user.nome}, Status: ${user.status}',
    after: 'Nome: ${user.nome} | Status: ${user.status} | ID: ${user.id}',
    expected: { smelly: 1, clean: 0 },
  },
];

const results = [];
for (const scenario of cases) {
  const normalized = source.replaceAll('\r\n', '\n');
  if (normalized.split(scenario.before).length !== 2) {
    throw new Error(`O trecho a alterar não é único: ${scenario.name}`);
  }
  const fixture = path.join(root, 'tmp', 'regressoes', scenario.name);
  for (const directory of ['src', 'test', '__tests__']) {
    fs.mkdirSync(path.join(fixture, directory), { recursive: true });
  }
  fs.writeFileSync(path.join(fixture, 'src/userService.js'),
    normalized.replace(scenario.before, scenario.after));
  fs.copyFileSync(path.join(root, 'test/userService.smelly.test.js'),
    path.join(fixture, 'test/userService.smelly.test.js'));
  fs.copyFileSync(path.join(root, '__tests__/userService.clean.test.js'),
    path.join(fixture, '__tests__/userService.clean.test.js'));

  for (const [suite, relative] of [
    ['smelly', 'test/userService.smelly.test.js'],
    ['clean', '__tests__/userService.clean.test.js'],
  ]) {
    const config = JSON.stringify({ rootDir: fixture, transform: {}, testEnvironment: 'node' });
    const result = spawnSync(process.execPath, [path.join(root, 'node_modules/jest/bin/jest.js'),
      '--config', config, '--runInBand', '--runTestsByPath', path.join(fixture, relative),
    ], { cwd: root, encoding: 'utf8', env: { ...process.env, FORCE_COLOR: '0' } });
    results.push({ cenario: scenario.name, suite, codigoSaida: result.status,
      codigoEsperado: scenario.expected[suite], saida: result.stdout + result.stderr });
  }
}

const output = path.join(root, 'docs/evidencias');
fs.mkdirSync(output, { recursive: true });
fs.writeFileSync(path.join(output, 'regressoes.json'), JSON.stringify(results, null, 2) + '\n');
const summary = results.map(result =>
  `${result.cenario} / ${result.suite}: saída ${result.codigoSaida}, esperada ${result.codigoEsperado}`
).join('\n');
fs.writeFileSync(path.join(output, 'regressoes.txt'), summary + '\n');
console.log(summary);
if (results.some(result => result.codigoSaida !== result.codigoEsperado)) {
  process.exitCode = 1;
}
