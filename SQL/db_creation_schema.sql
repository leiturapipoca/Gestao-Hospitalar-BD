DROP TRIGGER IF EXISTS TRG_BEFORE_DELETE_PACIENTE ON PACIENTE;
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
                      LIVRE BOOLEAN,
                      FOREIGN KEY (HOSPITAL) REFERENCES HOSPITAL
);

CREATE TABLE FUNCINARIO (
                            MATRICULA SERIAL PRIMARY KEY,
                            CPF CHAR(11) UNIQUE,
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
                         CNES_HOSP CHAR(7) REFERENCES HOSPITAL,
                         DESCRICAO TEXT
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


CREATE VIEW FUNC_COMPLETO AS (
                             SELECT FUNCINARIO.CPF, FUNCINARIO.NOME, FUNCINARIO.MATRICULA, FUNCAO.NOME AS F_NOME FROM FUNCINARIO
                                                                                                                          JOIN FUNCAO ON FUNCAO.ID = FUNCINARIO.FUNC);

-- Adiciona a coluna para guardar a imagem (Binário)
ALTER TABLE FUNCINARIO ADD COLUMN FOTO BYTEA;
ALTER TABLE PROCEDIMENTO ADD COLUMN ID_SALA INT REFERENCES SALA(ID);




-- 1. A Função que faz o serviço sujo
CREATE OR REPLACE FUNCTION FN_LIMPAR_DADOS_PACIENTE()
    RETURNS TRIGGER AS $$
BEGIN
    -- 1º: Apagar os vínculos de Médicos com Procedimentos (PROF_PROC)
    -- Isso é o "bisneto". Se não apagar, não dá pra apagar o Procedimento.
    DELETE FROM PROF_PROC
    WHERE COD_PROC IN (
        SELECT P.CODIGO
        FROM PROCEDIMENTO P
                 JOIN ENTRADA E ON P.COD_ENTR = E.CODIGO
        WHERE E.CPF_PAC = OLD.CPF
    );

    -- 2º: Apagar os Procedimentos (PROCEDIMENTO)
    -- Esses são os "netos" (filhos da Entrada)
    DELETE FROM PROCEDIMENTO
    WHERE COD_ENTR IN (
        SELECT CODIGO
        FROM ENTRADA
        WHERE CPF_PAC = OLD.CPF
    );

    -- 3º: Apagar as Entradas (ENTRADA)
    -- Esses são os "filhos" diretos
    DELETE FROM ENTRADA WHERE CPF_PAC = OLD.CPF;

    -- 4º: Apagar Doenças e Telefones (Outros filhos)
    DELETE FROM DOENCA WHERE PORTADOR = OLD.CPF;
    DELETE FROM TELEFONE WHERE PROPRIETARIO = OLD.CPF;

    -- 5º: Retorna OLD para permitir que o Paciente finalmente seja apagado
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TRG_BEFORE_DELETE_PACIENTE
    BEFORE DELETE ON PACIENTE
    FOR EACH ROW
EXECUTE FUNCTION FN_LIMPAR_DADOS_PACIENTE();

CREATE OR REPLACE PROCEDURE PR_REGISTRAR_PROCEDIMENTO_COMPLETO(
    p_cod_entrada INT,
    p_crm_medico CHAR(9),
    p_nome_procedimento TEXT,
    p_nome_doenca TEXT,
    p_numero_sala INT -- NOVO PARÂMETRO
)
    LANGUAGE plpgsql
AS $$
DECLARE
    v_cpf_paciente CHAR(11);
    v_cpf_medico CHAR(11);
    v_id_tipo_proc INT;
    v_novo_cod_proc INT;
    v_doenca_caps TEXT;
    v_cnes_hospital CHAR(7);
    v_id_sala INT;
BEGIN
    -- 1. Descobrir quem é o Paciente e qual o Hospital da Entrada
    SELECT CPF_PAC, CNES_HOSP INTO v_cpf_paciente, v_cnes_hospital
    FROM ENTRADA WHERE CODIGO = p_cod_entrada;

    IF v_cpf_paciente IS NULL THEN
        RAISE EXCEPTION 'Entrada % não encontrada.', p_cod_entrada;
    END IF;

    -- 2. Validar Sala (NOVO)
    -- Verifica se existe uma sala com esse número neste hospital
    SELECT ID INTO v_id_sala
    FROM SALA
    WHERE NUMERO = p_numero_sala AND HOSPITAL = v_cnes_hospital;

    IF v_id_sala IS NULL THEN
        RAISE EXCEPTION 'Sala número % não existe no hospital da entrada (%s).', p_numero_sala, v_cnes_hospital;
    END IF;

    -- Opcional: Verificar se a sala está livre (se tiver a coluna LIVRE)
     IF EXISTS (SELECT 1 FROM SALA WHERE ID = v_id_sala AND LIVRE = FALSE) THEN
        RAISE EXCEPTION 'Sala % está ocupada.', p_numero_sala;
     END IF;

    -- Opcional: Marcar sala como ocupada
     UPDATE SALA SET LIVRE = FALSE WHERE ID = v_id_sala;

    -- 3. Tratamento da Doença
    v_doenca_caps := UPPER(p_nome_doenca);
    IF NOT EXISTS (SELECT 1 FROM DOENCA WHERE DESCRICAO = v_doenca_caps AND PORTADOR = v_cpf_paciente) THEN
        INSERT INTO DOENCA (DESCRICAO, PORTADOR) VALUES (v_doenca_caps, v_cpf_paciente);
    END IF;

    -- 4. Validar Médico
    SELECT CPF INTO v_cpf_medico FROM PROFISSIONAL_SAUDE WHERE CRM_MED = p_crm_medico;
    IF v_cpf_medico IS NULL THEN
        RAISE EXCEPTION 'Médico com CRM % não encontrado.', p_crm_medico;
    END IF;

    -- 5. Validar Procedimento
    SELECT ID INTO v_id_tipo_proc FROM TIPO_PROC WHERE NOME = p_nome_procedimento;
    IF v_id_tipo_proc IS NULL THEN
        RAISE EXCEPTION 'Procedimento inválido.';
    END IF;

    -- 6. Inserir Procedimento
    -- Se você adicionou coluna ID_SALA em PROCEDIMENTO, adicione aqui no INSERT
    INSERT INTO PROCEDIMENTO (ID_TIPO, COD_ENTR)
    VALUES (v_id_tipo_proc, p_cod_entrada)
    RETURNING CODIGO INTO v_novo_cod_proc;

    -- 7. Vincular Médico
    INSERT INTO PROF_PROC (COD_PROC, COD_PROF) VALUES (v_novo_cod_proc, v_cpf_medico);

END;
$$;
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
    ('GRIPE', '00000000001'),
    ('HEMATOMAS', '00000000001'),
    ('POLIDACTILIA', '00000000001'),
    ('CICATRIZES', '00000000001'),
    ('ASMA', '00000000002');

INSERT INTO FUNCAO (NOME)
VALUES ('Recepcionista'), ('Secretário'), ('Diretor'), ('Superintendente'), ('Auditor');

INSERT INTO ADMINISTRADOR (NOME)
VALUES ('Admin 1'), ('Admin 2');

-- ============================
-- 2) HOSPITAL + SALAS
-- ============================

INSERT INTO HOSPITAL (CNES, NOME, ADM)
VALUES
    ('0000001', 'Hospital Central', 1),
    ('0000002', 'Hospital Norte', 1),
    ('0000003', 'Hospital Sul', 1),
    ('0000004', 'Hospital Leste', 1),
    ('0000005', 'Hospital Oeste', 1);

INSERT INTO SALA (NUMERO, HOSPITAL, LIVRE)
VALUES
    (101, '0000001', TRUE),
    (102, '0000001',TRUE),
    (103,'0000001',FALSE),
    (104,'0000001',TRUE),
    (105,'0000001',TRUE),

    (106, '0000002',TRUE),
    (107, '0000002',TRUE),
    (108,'0000002',TRUE),
    (109,'0000002',TRUE),
    (110,'0000002',TRUE),

    (111, '0000003',TRUE),
    (112, '0000003',TRUE),
    (113,'0000003',TRUE),
    (114,'0000003',TRUE),
    (115,'0000003',TRUE),

    (116, '0000004',TRUE),
    (117, '0000004',TRUE),
    (118,'0000004',TRUE),
    (119,'0000004',TRUE),
    (120,'0000004',TRUE),

    (121, '0000005',TRUE),
    (122, '0000005',TRUE),
    (123,'0000005',TRUE),
    (124,'0000005',TRUE),
    (125,'0000005',TRUE);


-- ============================
-- 3) FUNCIONARIOS
-- ============================

INSERT INTO FUNCINARIO (NOME, FUNC, SENHA, CPF)
VALUES
    ('Carlos Func', 1, 'abc','00000000000'),
    ('João Func', 2, 'abc','00000000001');

-- ============================
-- 4) MÉDICO, ENFERMEIRO, ESPECIALIDADE
-- ============================

INSERT INTO MEDICO (CRM)
VALUES ('CRM000001'),('CRM000002'),('CRM000003'),('CRM000004'),('CRM000005'), ('CRM000006') ;

INSERT INTO ENFERMEIRO (CODIGO)
VALUES (DEFAULT);  -- gera automaticamente (1)

INSERT INTO ESPECIALIDADE (NOME)
VALUES ('Cardiologia'), ('Pediatria'), ('Odontologia'), ('Radioterpia'), ('Oftalmologia');

-- ============================
-- 5) PROFISSIONAL DE SAÚDE
-- ============================

INSERT INTO PROFISSIONAL_SAUDE (CPF, NOME, TIPO, CRM_MED, COD_ENF)
VALUES
    ('00000000011', 'Dra. Maristela', 'M', 'CRM000001', NULL),
    ('00000000012', 'Dr. LeBron', 'M', 'CRM000002', NULL),
    ('00000000013', 'Dr. Shaquille', 'M', 'CRM000003', NULL),
    ('00000000014', 'Dr. Durant', 'M', 'CRM000004', NULL),
    ('00000000015', 'Dr. Bonifácio', 'M', 'CRM000005', NULL),
    ('00000000016', 'Dr. Karl-Anthony', 'M', 'CRM000006', NULL),
     ('00000000031', 'Enf. Beltrano', 'E', NULL, 1);

INSERT INTO PROF_SAUDE_HOSP (CPF_PROF, CNES_HOSP)
VALUES
    ('00000000011', '0000001'),
    ('00000000012', '0000002'),
    ('00000000013', '0000003'),
    ('00000000014', '0000004'),
    ('00000000015', '0000005'),
    ('00000000016', '0000001');


-- ============================
-- 6) TIPOS DE PROCEDIMENTOS + ENTRADA
-- ============================

INSERT INTO TIPO_PROC (NOME)
VALUES
    ('Raio-X'),
    ('Curativo'),
    ('Tomografia'),
    ('Ultrassom'),
    ('Ressonância Magnética'),
    ('Exame de Sangue'),
    ('Eletrocardiograma'),
    ('Endoscopia'),
    ('Consulta');

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
    (2, 2),
    (1, 2),
    (2, 1),
    (1, 1),
    (2, 2),
    (3, 1),
    (4, 1),
    (5, 2),
    (6, 1),
    (7, 2),
    (8, 1),
    (3, 2),
    (4, 2);

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
    ('CRM000001', 2),
    ('CRM000002',3),
    ('CRM000003',4),
    ('CRM000004',5),
    ('CRM000002',2);


SELECT * FROM SALA;
