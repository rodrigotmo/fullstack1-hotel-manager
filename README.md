# Projeto de um gerenciador de hotel para a disciplina de Fullstack I das Faculdades Integradas de Taquara.
# Time de devs -> Guilherme Staffen, Thauã Reichert, Rodrigo Machado
# fullstack1-hotel-manager


```mermaid
erDiagram
    FUNCIONARIO {
        int id_funcionario PK
        string nome
        string cargo
        string telefone
        string email
    }

    QUARTO {
        int id_quarto PK
        string numero
        string tipo
        string status
    }

    CLIENTE {
        int id_cliente PK
        string nome
        string documento
        string telefone
        string email
    }

    RESERVA {
        int id_reserva PK
        date data_reserva
        date data_check_in
        date data_check_out
        int id_cliente FK
        int id_funcionario FK
        int id_quarto FK
    }

    FUNCIONARIO }|--o{ RESERVA : "gerencia"
    CLIENTE ||--o{ RESERVA : "realiza"
    QUARTO ||--o{ RESERVA : "associado a"
```