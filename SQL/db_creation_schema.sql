
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE PACIENTE (
                          CPF CHAR(11) PRIMARY KEY,
                          DT_NASC DATE,
                          SEXO CHAR(1) NOT NULL,
                          NOME TEXT NOT NULL,
                          SENHA TEXT,
                          TIPO_SANG CHAR(2)
);

CREATE TABLE TELEFONE(
                         NUMERO TEXT,
                         PROPRIETARIO CHAR(11) REFERENCES PACIENTE,
                         PRIMARY KEY (NUMERO, PROPRIETARIO)
);

CREATE TABLE DOENCA(
                       DESCRICAO TEXT,
                       PORTADOR CHAR(11) REFERENCES PACIENTE,
                       PRIMARY KEY (DESCRICAO, PORTADOR)
);

CREATE TABLE FUNCAO (
                        ID SERIAL PRIMARY KEY,
                        NOME TEXT NOT NULL
);

CREATE TABLE ADMINISTRADOR (
                               ID SERIAL PRIMARY KEY,
                               NOME TEXT NOT NULL
);

CREATE TABLE HOSPITAL (
                          CNES CHAR(7) PRIMARY KEY,
                          NOME TEXT NOT NULL,
                          ADM SERIAL NOT NULL,
                          PROCEDIMENTOS SERIAL NOT NULL,
                          FOREIGN KEY (ADM) REFERENCES ADMINISTRADOR
);

CREATE TABLE SALA (
                      ID SERIAL PRIMARY KEY,
                      NUMERO SERIAL,
                      HOSPITAL CHAR(7),
                      FOREIGN KEY (HOSPITAL) REFERENCES HOSPITAL
);

CREATE TABLE FUNCINARIO (
                            MATRICULA SERIAL PRIMARY KEY,
                            NOME TEXT NOT NULL,
                            FUNC SERIAL NOT NULL,
                            SENHA TEXT NOT NULL,
                            FOREIGN KEY (FUNC) REFERENCES FUNCAO
);

CREATE TABLE MEDICO (
                        CRM CHAR(9) PRIMARY KEY

);

CREATE TABLE ENFERMEIRO(
                           CODIGO SERIAL PRIMARY KEY

);

CREATE TABLE ESPECIALIDADE(
                              ID SERIAL PRIMARY KEY,
                              NOME TEXT NOT NULL
);

CREATE TABLE PROFISSIONAL_SAUDE (
                                    CPF CHAR(11) PRIMARY KEY,
                                    NOME TEXT NOT NULL,
                                    TIPO CHAR(1), -- M ou E
                                    SENHA TEXT NOT NULL,
                                    CRM_MED CHAR(9) REFERENCES MEDICO ON DELETE SET NULL,
                                    COD_ENF INTEGER REFERENCES ENFERMEIRO ON DELETE SET NULL
);

CREATE TABLE PROF_SAUDE_HOSP (
                                 CPF_PROF CHAR(11) REFERENCES PROFISSIONAL_SAUDE,
                                 CNES_HOSP CHAR(7) REFERENCES HOSPITAL,
                                 PRIMARY KEY (CPF_PROF, CNES_HOSP)
);

CREATE TABLE TIPO_PROC (
                           ID SERIAL PRIMARY KEY,
                           NOME TEXT NOT NULL
);

CREATE TABLE ENTRADA (
                         CODIGO SERIAL PRIMARY KEY,
                         DATA TIMESTAMP,
                         CPF_PAC CHAR(11) REFERENCES PACIENTE,
                         CNES_HOSP CHAR(7) REFERENCES HOSPITAL
);

CREATE TABLE PROCEDIMENTO (
                              CODIGO SERIAL PRIMARY KEY,
                              ID_TIPO SERIAL REFERENCES TIPO_PROC,
                              COD_ENTR SERIAL REFERENCES ENTRADA
);

-- TABLAS RELACIONAIS
CREATE TABLE FUNC_HOSP (
                           CNES_HOSP CHAR(7) REFERENCES HOSPITAL,
                           MATR_FUNC SERIAL REFERENCES FUNCINARIO,
                           PRIMARY KEY (CNES_HOSP, MATR_FUNC)
);

CREATE TABLE PROF_PROC (
                           COD_PROC SERIAL REFERENCES PROCEDIMENTO,
                           COD_PROF CHAR(11) REFERENCES PROFISSIONAL_SAUDE,
                           PRIMARY KEY (COD_PROF,COD_PROC)
);

CREATE TABLE MEDICO_ESPEC (
                              CRM_MED CHAR(9) REFERENCES MEDICO,
                              ID_SPEC SERIAL REFERENCES ESPECIALIDADE,
                              PRIMARY KEY (CRM_MED, ID_SPEC)
);

-- ============================
-- 1) TABELAS BÁSICAS
-- ============================

INSERT INTO PACIENTE (CPF, DT_NASC, SEXO, NOME, SENHA, TIPO_SANG)
VALUES
    ('00000000001', '2000-01-01', 'M', 'Paciente A', '123', 'A+'),
    ('00000000002', '1999-05-10', 'F', 'Paciente B', '123', 'O-');

INSERT INTO TELEFONE (NUMERO, PROPRIETARIO)
VALUES
    ('1111-1111', '00000000001'),
    ('2222-2222', '00000000002');

INSERT INTO DOENCA (DESCRICAO, PORTADOR)
VALUES
    ('Gripe', '00000000001'),
    ('Asma', '00000000002');

INSERT INTO FUNCAO (NOME)
VALUES ('Recepcionista'), ('Segurança');

INSERT INTO ADMINISTRADOR (NOME)
VALUES ('Admin 1'), ('Admin 2');

-- ============================
-- 2) HOSPITAL + SALAS
-- ============================

INSERT INTO HOSPITAL (CNES, NOME, ADM)
VALUES
    ('0000001', 'Hospital Central', 1);

INSERT INTO SALA (NUMERO, HOSPITAL)
VALUES
    (101, '0000001'),
    (102, '0000001');

-- ============================
-- 3) FUNCIONARIOS
-- ============================

INSERT INTO FUNCINARIO (NOME, FUNC, SENHA)
VALUES
    ('Carlos Func', 1, 'abc'),
    ('João Func', 2, 'abc');

-- ============================
-- 4) MÉDICO, ENFERMEIRO, ESPECIALIDADE
-- ============================

INSERT INTO MEDICO (CRM)
VALUES ('CRM000001');

INSERT INTO ENFERMEIRO (CODIGO)
VALUES (DEFAULT);  -- gera automaticamente (1)

INSERT INTO ESPECIALIDADE (NOME)
VALUES ('Cardiologia'), ('Pediatria');

-- ============================
-- 5) PROFISSIONAL DE SAÚDE
-- ============================

INSERT INTO PROFISSIONAL_SAUDE (CPF, NOME, TIPO, SENHA, CRM_MED, COD_ENF)
VALUES
    ('00000000011', 'Dr. Fulano', 'M', 'med123', 'CRM000001', NULL),
    ('00000000012', 'Enf. Beltrano', 'E', 'enf123', NULL, 1);

INSERT INTO PROF_SAUDE_HOSP (CPF_PROF, CNES_HOSP)
VALUES
    ('00000000011', '0000001'),
    ('00000000012', '0000001');

-- ============================
-- 6) TIPOS DE PROCEDIMENTOS + ENTRADA
-- ============================

INSERT INTO TIPO_PROC (NOME)
VALUES
    ('Raio-X'),
    ('Curativo');

INSERT INTO ENTRADA (DATA, CPF_PAC, CNES_HOSP)
VALUES
    ('2024-01-01 08:00', '00000000001', '0000001'),
    ('2024-01-02 09:00', '00000000002', '0000001');

-- ============================
-- 7) PROCEDIMENTO
-- ============================

INSERT INTO PROCEDIMENTO (ID_TIPO, COD_ENTR)
VALUES
    (1, 1),
    (2, 2);

-- ============================
-- 8) TABELAS RELACIONAIS
-- ============================

INSERT INTO FUNC_HOSP (CNES_HOSP, MATR_FUNC)
VALUES
    ('0000001', 1),
    ('0000001', 2);

INSERT INTO PROF_PROC (COD_PROC, COD_PROF)
VALUES
    (1, '00000000011'),
    (2, '00000000012');

INSERT INTO MEDICO_ESPEC (CRM_MED, ID_SPEC)
VALUES
    ('CRM000001', 1),
    ('CRM000001', 2);

