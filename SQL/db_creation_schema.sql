DROP TABLE IF EXISTS SLA;


DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE PACIENTE (
                          CPF CHAR(11) PRIMARY KEY,
                          DT_NASC DATE,
                          SEXO CHAR(1) NOT NULL,
                          NOME TEXT NOT NULL,
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
                          FOREIGN KEY (ADM) REFERENCES ADMINISTRADOR
);

CREATE TABLE SALA (
                      ID SERIAL PRIMARY KEY,
                      NUMERO SERIAL,
                      HOSPITAL CHAR(7),
                      FOREIGN KEY (HOSPITAL) REFERENCES HOSPITAL
);

CREATE TABLE FUNCIONARIO (
                            MATRICULA SERIAL PRIMARY KEY,
                            NOME TEXT NOT NULL,
                            FUNC SERIAL NOT NULL,
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
                           MATR_FUNC SERIAL REFERENCES FUNCIONARIO,
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
CREATE TABLE USUARIO (
        ID INT PRIMARY KEY,
        SENHA CHAR(9)
);


INSERT INTO USUARIO VALUES (1, '123456789');
INSERT INTO MEDICO(CRM) VALUES ('1234567DF');
INSERT INTO ENFERMEIRO(CODIGO) VALUES (1);
INSERT INTO PROFISSIONAL_SAUDE(CPF, NOME, TIPO, CRM_MED, COD_ENF) VALUES ('03191571647', 'CARLOS', 'M', '1234567DF', NULL);
-- ============================
-- PACIENTES
-- ============================
INSERT INTO PACIENTE (CPF, DT_NASC, SEXO, NOME, TIPO_SANG) VALUES
                                                               ('00000000001', '1990-01-10', 'M', 'João Silva', 'A+'),
                                                               ('00000000002', '1985-05-20', 'F', 'Maria Souza', 'O-'),
                                                               ('00000000003', '2000-12-03', 'M', 'Pedro Almeida', 'B+'),
                                                               ('00000000004', '1975-03-15', 'F', 'Ana Costa', 'AB');

-- ============================
-- TELEFONES
-- ============================
INSERT INTO TELEFONE VALUES
                         ('1111-1111', '00000000001'),
                         ('2222-2222', '00000000002'),
                         ('3333-3333', '00000000003'),
                         ('4444-4444', '00000000004');

-- ============================
-- DOENÇAS
-- ============================
INSERT INTO DOENCA VALUES
                       ('Asma', '00000000001'),
                       ('Diabetes', '00000000002'),
                       ('Hipertensão', '00000000004');

-- ============================
-- FUNÇÕES DE FUNCIONÁRIOS
-- ============================
INSERT INTO FUNCAO (NOME) VALUES
                              ('Recepcionista'),
                              ('Segurança'),
                              ('Auxiliar administrativo');

-- ============================
-- ADMINISTRADORES
-- ============================
INSERT INTO ADMINISTRADOR (NOME) VALUES
                                     ('Carlos Admin'),
                                     ('Fernanda Admin');

-- ============================
-- HOSPITAIS
-- ============================
INSERT INTO HOSPITAL (CNES, NOME, ADM) VALUES
                                           ('0000001', 'Hospital Central', 1),
                                           ('0000002', 'Hospital Municipal', 2);

-- ============================
-- SALAS
-- ============================
INSERT INTO SALA (NUMERO, HOSPITAL) VALUES
                                        (101, '0000001'),
                                        (102, '0000001'),
                                        (201, '0000002');

-- ============================
-- FUNCIONÁRIOS
-- ============================
INSERT INTO FUNCIONARIO (NOME, FUNC) VALUES
                                         ('Paulo Recepcionista', 1),
                                         ('José Segurança', 2),
                                         ('Clara Auxiliar', 3);

-- ============================
-- MEDICOS / ENFERMEIROS
-- ============================
INSERT INTO MEDICO (CRM) VALUES ('1111111AA');
INSERT INTO MEDICO (CRM) VALUES ('2222222BB');

INSERT INTO ENFERMEIRO (CODIGO) VALUES (10), (20);

-- ============================
-- PROFISSIONAIS DE SAÚDE
-- ============================
INSERT INTO PROFISSIONAL_SAUDE VALUES
                                   ('00000000010', 'Dr. Alberto', 'M', '1111111AA', NULL),
                                   ('00000000011', 'Dr. Helena', 'M', '2222222BB', NULL),
                                   ('00000000012', 'Enf. Marcos', 'E', NULL, 10),
                                   ('00000000013', 'Enf. Julia', 'E', NULL, 20);

-- ============================
-- PROFISSIONAIS EM HOSPITAIS
-- ============================
INSERT INTO PROF_SAUDE_HOSP VALUES
                                ('00000000010', '0000001'),
                                ('00000000011', '0000001'),
                                ('00000000012', '0000002'),
                                ('00000000013', '0000002');

-- ============================
-- ESPECIALIDADES
-- ============================
INSERT INTO ESPECIALIDADE (NOME) VALUES
                                     ('Cardiologia'),
                                     ('Ortopedia'),
                                     ('Pediatria');

-- Médicos com especialidades
INSERT INTO MEDICO_ESPEC VALUES
                             ('1111111AA', 1),
                             ('1111111AA', 3),
                             ('2222222BB', 2);

-- ============================
-- TIPOS DE PROCEDIMENTOS
-- ============================
INSERT INTO TIPO_PROC (NOME) VALUES
                                 ('Raio-X'),
                                 ('Cirurgia'),
                                 ('Curativo');

-- ============================
-- ENTRADAS
-- ============================
INSERT INTO ENTRADA (DATA, CPF_PAC, CNES_HOSP) VALUES
                                                   ('2025-01-10 08:30', '00000000001', '0000001'),
                                                   ('2025-01-10 09:00', '00000000002', '0000002'),
                                                   ('2025-01-10 10:15', '00000000003', '0000001');

-- ============================
-- PROCEDIMENTOS
-- ============================
INSERT INTO PROCEDIMENTO (ID_TIPO, COD_ENTR) VALUES
                                                 (1, 1), -- Raio-X para paciente 1
                                                 (3, 1), -- Curativo paciente 1
                                                 (2, 2), -- Cirurgia paciente 2
                                                 (1, 3); -- Raio-X paciente 3

-- ============================
-- PROFISSIONAIS EM PROCEDIMENTOS
-- ============================
INSERT INTO PROF_PROC VALUES
                          (1, '00000000010'),
                          (1, '00000000012'),
                          (2, '00000000011'),
                          (3, '00000000012'),
                          (4, '00000000013');

-- ============================
-- FUNCIONÁRIOS EM HOSPITAIS
-- ============================
INSERT INTO FUNC_HOSP VALUES
                          ('0000001', 1),
                          ('0000001', 2),
                          ('0000002', 3);
