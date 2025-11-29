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
