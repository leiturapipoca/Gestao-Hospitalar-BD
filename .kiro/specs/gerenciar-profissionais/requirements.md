# Requirements Document

## Introduction

This feature implements a management interface for health professionals (profissionais de saúde) in the hospital system. It follows the same pattern as the existing employee management feature (GerenciarFuncs), providing functionality to add, remove, and query health professionals. Health professionals include both doctors (médicos) and nurses (enfermeiros), each with their own unique identifiers (CRM for doctors, CODIGO for nurses).

## Glossary

- **System**: The hospital management application
- **Health Professional (Profissional de Saúde)**: A medical professional who can be either a doctor or a nurse
- **Doctor (Médico)**: A health professional with type 'M' and a CRM identifier
- **Nurse (Enfermeiro)**: A health professional with type 'E' and a CODIGO identifier
- **CPF**: Brazilian individual taxpayer registry identification (11 digits)
- **CRM**: Regional Medical Council registration number (9 characters)
- **Management Interface**: The main screen that provides navigation to add, remove, and query operations
- **User**: An internal system user (funcionário) who has permission to manage health professionals
- **Database**: The PostgreSQL database storing all system data

## Requirements

### Requirement 1

**User Story:** As an internal user, I want to access a health professional management interface, so that I can perform administrative operations on health professional records.

#### Acceptance Criteria

1. WHEN the user navigates from the internal menu to the health professional management option THEN the System SHALL display the health professional management interface
2. WHEN the management interface is displayed THEN the System SHALL show buttons for adding, removing, and querying health professionals
3. WHEN the management interface is displayed THEN the System SHALL show a button to return to the previous screen
4. WHEN the user clicks the return button THEN the System SHALL navigate back to the internal menu and preserve the user session data

### Requirement 2

**User Story:** As an internal user, I want to add new health professionals to the system, so that I can register doctors and nurses who work at the hospital.

#### Acceptance Criteria

1. WHEN the user clicks the add health professional button THEN the System SHALL display the add health professional screen
2. WHEN the add screen is displayed THEN the System SHALL provide input fields for CPF, name, professional type, and type-specific identifiers
3. WHEN the user submits valid health professional data THEN the System SHALL insert the new record into the PROFISSIONAL_SAUDE table
4. WHEN the professional type is doctor THEN the System SHALL require a valid CRM and insert a record into the MEDICO table
5. WHEN the professional type is nurse THEN the System SHALL require a valid CODIGO and insert a record into the ENFERMEIRO table
6. WHEN the user submits incomplete or invalid data THEN the System SHALL display an error message and prevent database insertion

### Requirement 3

**User Story:** As an internal user, I want to remove health professionals from the system, so that I can delete records of professionals who no longer work at the hospital.

#### Acceptance Criteria

1. WHEN the user clicks the remove health professional button THEN the System SHALL display the remove health professional screen
2. WHEN the remove screen is displayed THEN the System SHALL provide an input field for the health professional CPF
3. WHEN the user submits a valid CPF that exists in the database THEN the System SHALL delete the health professional record from the PROFISSIONAL_SAUDE table
4. WHEN the health professional is deleted THEN the System SHALL handle cascading deletions or set null operations for related records
5. WHEN the user submits a CPF that does not exist THEN the System SHALL display an error message indicating the professional was not found

### Requirement 4

**User Story:** As an internal user, I want to query health professional information, so that I can view details about doctors and nurses in the system.

#### Acceptance Criteria

1. WHEN the user clicks the query health professional button THEN the System SHALL display the query health professional screen
2. WHEN the query screen is displayed THEN the System SHALL provide an input field for the health professional CPF
3. WHEN the user submits a valid CPF that exists in the database THEN the System SHALL retrieve and display the professional's information including name, type, and type-specific identifier
4. WHEN the professional is a doctor THEN the System SHALL display the CRM number
5. WHEN the professional is a nurse THEN the System SHALL display the CODIGO number
6. WHEN the user submits a CPF that does not exist THEN the System SHALL display a message indicating no professional was found

### Requirement 5

**User Story:** As a system architect, I want the health professional management feature to follow the existing MVC pattern, so that the codebase remains consistent and maintainable.

#### Acceptance Criteria

1. WHEN implementing the feature THEN the System SHALL create a GerenciarProfsController following the same structure as GerenciarFuncsController
2. WHEN implementing the feature THEN the System SHALL create view classes (TelaGerenciarProfs, TelaAdicionarProf, TelaConsultarProf, TelaRemoverProf) following the existing view pattern
3. WHEN implementing the feature THEN the System SHALL extend ProfissionalDAO with methods for add, remove, and query operations
4. WHEN implementing controllers THEN the System SHALL use callback functions to handle button actions
5. WHEN navigating between screens THEN the System SHALL properly destroy the previous frame before creating the new one

### Requirement 6

**User Story:** As a developer, I want proper error handling and logging, so that I can debug issues and ensure system reliability.

#### Acceptance Criteria

1. WHEN any database operation is performed THEN the System SHALL log the operation using the Python logging module
2. WHEN a database error occurs THEN the System SHALL catch the exception and display a user-friendly error message
3. WHEN a user action is performed THEN the System SHALL log the action with appropriate detail level
4. WHEN an error occurs THEN the System SHALL log the error with sufficient context for debugging
5. WHEN database connections are used THEN the System SHALL properly close connections to prevent resource leaks
