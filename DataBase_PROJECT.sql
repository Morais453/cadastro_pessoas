-- Criar o banco de dados
CREATE DATABASE cadastro_pessoas;

-- Usar o banco de dados recém-criado
USE cadastro_pessoas;

-- Criar a tabela pessoas
CREATE TABLE pessoas (
    id INT AUTO_INCREMENT PRIMARY KEY,      -- ID autoincrementável e chave primária
    nome VARCHAR(100) NOT NULL,             -- Nome da pessoa
    endereco VARCHAR(200) NOT NULL,         -- Endereço da pessoa
    telefone VARCHAR(15) NOT NULL,          -- Telefone da pessoa
    tipo_servico VARCHAR(100) NOT NULL,     -- Tipo de serviço prestado pela pessoa
    data_cadastro DATE NOT NULL,            -- Data de cadastro
    status_servico ENUM('Em andamento', 'Concluído') NOT NULL  -- Status do serviço
);
