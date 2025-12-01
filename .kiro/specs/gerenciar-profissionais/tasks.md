# Implementation Plan

- [x] 1. Create the main management view (TelaGerenciarProfs)
  - Create `View/TelaGerenciarProfs.py` with a frame containing four buttons
  - Add button: "Adicionar profissional de saúde"
  - Add button: "Remover profissional de saúde"
  - Add button: "Consultar informações de profissional"
  - Add button: "Voltar"
  - Implement setter methods for button callbacks
  - Follow the same structure as `TelaGerenciarFuncs.py`
  - _Requirements: 1.2, 1.3_

- [x] 2. Create the add professional view (TelaAdicionarProf)
  - Create `View/TelaAdicionarProf.py` with a frame and basic structure
  - Add label and entry field for CPF
  - Add label and entry field for Nome
  - Add label and dropdown/radio buttons for Tipo (M/E)
  - Add conditional entry fields for CRM (shown when type is M)
  - Add conditional entry fields for CODIGO (shown when type is E)
  - Add "Adicionar" button (placeholder action)
  - Add "Voltar" button
  - Follow the same structure as `TelaAdicionarFunc.py`
  - _Requirements: 2.2_

- [x] 3. Create the remove professional view (TelaRemoverProf)
  - Create `View/TelaRemoverProf.py` with a frame and basic structure
  - Add label and entry field for CPF
  - Add "Remover" button (placeholder action)
  - Add "Voltar" button
  - Add label for status messages
  - Follow the same structure as `TelaRemoverFunc.py`
  - _Requirements: 3.2_

- [x] 4. Create the query professional view (TelaConsultarProf)
  - Create `View/TelaConsultarProf.py` with a frame and basic structure
  - Add label and entry field for CPF
  - Add "Consultar" button (placeholder action)
  - Add "Voltar" button
  - Add frame/labels for displaying results (name, type, CRM/CODIGO)
  - Follow the same structure as `TelaConsultarFunc.py`
  - Keep the UI empty for now
  - _Requirements: 4.2_

- [x] 5. Create the main controller (GerenciarProfsController)
  - Create `Controller/GerenciarProfsController.py`
  - Implement `__init__` method that accepts root window and user session data
  - Initialize with TelaGerenciarProfs view
  - Implement `config_tela_gerenciar_profs_callbacks` method to wire up button callbacks
  - Implement `select_adicionar_prof` method to navigate to add screen
  - Implement `select_remover_prof` method to navigate to remove screen
  - Implement `select_consultar_prof` method to navigate to query screen
  - Implement `voltar` method to return to InternosController with session data
  - Ensure proper frame destruction before creating new views
  - Add logging for all navigation actions
  - Follow the same structure as `GerenciarFuncsController.py`
  - _Requirements: 1.1, 1.4, 5.1, 5.4, 5.5, 6.3_

- [x] 6. Integrate with InternosController
  - Update `Controller/InternosController.py`
  - Uncomment or update the `abrir_profissionais` method
  - Import GerenciarProfsController
  - Call GerenciarProfsController with root window and user session data
  - Ensure proper frame destruction before navigation
  - _Requirements: 1.1, 1.4_

- [x] 7. Add placeholder action handlers in controller
  - In GerenciarProfsController: Add `handle_adicionar_prof` method (log action only, display placeholder success message)
  - In GerenciarProfsController: Add `handle_remover_prof` method (log action only, display placeholder success message)
  - In GerenciarProfsController: Add `handle_consultar_prof` method (log action only, display placeholder results)
  - Wire these handlers to the respective view buttons
  - Log all button actions with appropriate detail
  - _Requirements: 6.3_

- [ ] 8. Final checkpoint - Manual testing
  - Ensure all tests pass, ask the user if questions arise
  - Manually test navigation from internal menu to professional management
  - Verify all buttons navigate to correct screens
  - Verify return button goes back to internal menu
  - Verify user session data is preserved
  - Verify all actions are logged
  - Check that no UI errors occur during navigation

## Phase 2: Database Integration

- [x] 9. Implement add_profissional method in ProfissionalDAO
  - Add method signature: `add_profissional(self, cpf: str, nome: str, tipo: str, crm: str = None, codigo: int = None) -> tuple[bool, str]`
  - Insert record into MEDICO table if tipo is 'M' (using CRM as primary key)
  - Insert record into ENFERMEIRO table if tipo is 'E' (CODIGO is auto-generated SERIAL)
  - Insert record into PROFISSIONAL_SAUDE table with CPF, NOME, TIPO, and appropriate foreign key (CRM_MED or COD_ENF)
  - Handle UniqueViolation exception for duplicate CPF
  - Return tuple (success: bool, message: str) similar to FuncionarioDAO.add_funcionario
  - Use parameterized queries to prevent SQL injection
  - Commit transaction on success, rollback on error
  - _Requirements: 2.3, 2.4, 2.5, 2.6_

- [x] 10. Implement remove_profissional method in ProfissionalDAO
  - Add method signature: `remove_profissional(self, cpf: str) -> tuple[bool, str]`
  - Check if professional exists before attempting deletion
  - Delete from PROF_PROC table (cascading relationship)
  - Delete from PROFISSIONAL_SAUDE table (cascading will handle MEDICO/ENFERMEIRO due to ON DELETE SET NULL)
  - Handle case where CPF does not exist
  - Return tuple (success: bool, message: str)
  - Use parameterized queries to prevent SQL injection
  - Commit transaction on success, rollback on error
  - Log all operations
  - _Requirements: 3.3, 3.4, 3.5_

- [x] 11. Implement consultar_profissional method in ProfissionalDAO
  - Add method signature: `consultar_profissional(self, cpf: str) -> dict | None`
  - Query PROFISSIONAL_SAUDE table by CPF
  - Return dictionary with keys: 'cpf', 'nome', 'tipo', 'crm' (if tipo='M'), 'codigo' (if tipo='E')
  - Return None if professional not found
  - Use parameterized queries to prevent SQL injection
  - Handle database errors gracefully
  - Log query operations
  - _Requirements: 4.3, 4.4, 4.5, 4.6_

- [x] 12. Update GerenciarProfsController to use ProfissionalDAO
  - Import ProfissionalDAO in GerenciarProfsController
  - Initialize ProfissionalDAO instance in __init__ method
  - Update handle_adicionar_prof to call DAO.add_profissional with form data
  - Validate form data before calling DAO (CPF length, nome not empty, CRM/CODIGO based on tipo)
  - Display success or error messages using view methods
  - Update handle_remover_prof to call DAO.remove_profissional
  - Display success or error messages using view methods
  - Update handle_consultar_prof to call DAO.consultar_profissional
  - Display results or error messages using view methods
  - Add proper error handling with try-except blocks
  - _Requirements: 2.2, 2.3, 3.2, 3.3, 4.2, 4.3, 6.1, 6.2_

- [ ] 13. Final checkpoint - Integration testing
  - Ensure all tests pass, ask the user if questions arise
  - Test adding a new doctor (tipo='M') with valid CRM
  - Test adding a new nurse (tipo='E') with valid CODIGO
  - Test adding professional with duplicate CPF (should show error)
  - Test adding professional with missing required fields (should show error)
  - Test removing an existing professional
  - Test removing non-existent professional (should show error)
  - Test querying an existing professional (verify all data displays correctly)
  - Test querying non-existent professional (should show error message)
  - Verify all database operations are logged
  - Verify database connections are properly closed
