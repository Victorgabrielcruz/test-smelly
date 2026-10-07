const { UserService } = require('../src/userService');

describe('UserService - testes de comportamento', () => {
  let userService;

  beforeEach(() => {
    userService = new UserService();
    userService._clearDB();
  });

  describe('createUser', () => {
    test('deve criar um usuário ativo com os dados informados', () => {
      // Arrange
      const nome = 'Alice';
      const email = 'alice@teste.com';
      const idade = 28;

      // Act
      const usuario = userService.createUser(nome, email, idade);

      // Assert
      expect(usuario).toEqual({
        id: expect.any(String),
        nome,
        email,
        idade,
        isAdmin: false,
        createdAt: expect.any(Date),
        status: 'ativo',
      });
      expect(usuario.id).not.toBe('');
    });

    test('deve criar um administrador quando solicitado', () => {
      // Arrange
      const nome = 'Admin';
      const email = 'admin@teste.com';
      const idade = 40;

      // Act
      const usuario = userService.createUser(nome, email, idade, true);

      // Assert
      expect(usuario.isAdmin).toBe(true);
    });

    test('deve atribuir IDs diferentes a usuários com os mesmos dados', () => {
      // Arrange
      const usuarioExistente = userService.createUser('Alice', 'alice@teste.com', 28);

      // Act
      const novoUsuario = userService.createUser('Alice', 'alice@teste.com', 28);

      // Assert
      expect(novoUsuario.id).not.toBe(usuarioExistente.id);
    });

    test('deve aceitar um usuário com exatamente 18 anos', () => {
      // Arrange
      const nome = 'Maior';
      const email = 'maior@teste.com';
      const idadeMinima = 18;

      // Act
      const usuario = userService.createUser(nome, email, idadeMinima);

      // Assert
      expect(usuario.idade).toBe(idadeMinima);
    });

    test('deve rejeitar um usuário com 17 anos', () => {
      // Arrange
      const nome = 'Menor';
      const email = 'menor@teste.com';
      const idade = 17;

      // Act
      const criarUsuario = () => userService.createUser(nome, email, idade);

      // Assert
      expect(criarUsuario).toThrow('O usuário deve ser maior de idade.');
    });

    test.each([
      ['nome', undefined, 'alice@teste.com', 28],
      ['email', 'Alice', undefined, 28],
      ['idade', 'Alice', 'alice@teste.com', undefined],
    ])('deve rejeitar a criação quando falta %s', (_campo, nome, email, idade) => {
      // Arrange: os argumentos são fornecidos pela tabela de cenários.

      // Act
      const criarUsuario = () => userService.createUser(nome, email, idade);

      // Assert
      expect(criarUsuario).toThrow('Nome, email e idade são obrigatórios.');
    });
  });

  describe('getUserById', () => {
    test('deve retornar os dados do usuário cadastrado pelo ID', () => {
      // Arrange
      const usuario = userService.createUser('Alice', 'alice@teste.com', 28);

      // Act
      const resultado = userService.getUserById(usuario.id);

      // Assert
      expect(resultado).toEqual(usuario);
    });

    test('deve retornar null para um ID inexistente', () => {
      // Arrange
      const idInexistente = 'usuario-inexistente';

      // Act
      const resultado = userService.getUserById(idInexistente);

      // Assert
      expect(resultado).toBeNull();
    });
  });

  describe('deactivateUser', () => {
    test('deve desativar um usuário comum e preservar seu cadastro', () => {
      // Arrange
      const usuario = userService.createUser('Comum', 'comum@teste.com', 30);
      const cadastroOriginal = { ...usuario };

      // Act
      const resultado = userService.deactivateUser(usuario.id);

      // Assert
      expect(resultado).toBe(true);
      expect(userService.getUserById(usuario.id)).toEqual({
        ...cadastroOriginal,
        status: 'inativo',
      });
    });

    test('deve recusar a desativação de um administrador e mantê-lo ativo', () => {
      // Arrange
      const administrador = userService.createUser('Admin', 'admin@teste.com', 40, true);
      const cadastroOriginal = { ...administrador };

      // Act
      const resultado = userService.deactivateUser(administrador.id);

      // Assert
      expect(resultado).toBe(false);
      expect(userService.getUserById(administrador.id)).toEqual(cadastroOriginal);
    });

    test('deve retornar false ao tentar desativar um ID inexistente', () => {
      // Arrange
      const idInexistente = 'usuario-inexistente';

      // Act
      const resultado = userService.deactivateUser(idInexistente);

      // Assert
      expect(resultado).toBe(false);
    });
  });

  describe('generateUserReport', () => {
    test('deve informar que não há usuários cadastrados', () => {
      // Arrange: o beforeEach deixa o banco vazio.

      // Act
      const relatorio = userService.generateUserReport();

      // Assert
      expect(relatorio).toMatch(/Nenhum usuário cadastrado/i);
    });

    test('deve incluir os IDs e nomes de todos os usuários cadastrados', () => {
      // Arrange
      const alice = userService.createUser('Alice', 'alice@teste.com', 28);
      const bob = userService.createUser('Bob', 'bob@teste.com', 32);

      // Act
      const relatorio = userService.generateUserReport();

      // Assert
      expect(relatorio).toContain(alice.id);
      expect(relatorio).toContain(alice.nome);
      expect(relatorio).toContain(bob.id);
      expect(relatorio).toContain(bob.nome);
    });

    test('deve informar o status ativo de um usuário recém-criado', () => {
      // Arrange
      userService.createUser('Alice', 'alice@teste.com', 28);

      // Act
      const relatorio = userService.generateUserReport();

      // Assert
      expect(relatorio).toContain('ativo');
      expect(relatorio).not.toContain('inativo');
    });

    test('deve refletir o status inativo após a desativação', () => {
      // Arrange
      const usuario = userService.createUser('Alice', 'alice@teste.com', 28);
      userService.deactivateUser(usuario.id);

      // Act
      const relatorio = userService.generateUserReport();

      // Assert
      expect(relatorio).toContain(usuario.id);
      expect(relatorio).toContain('inativo');
    });
  });
});
