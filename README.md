# Projeto de um sistema gerenciador de hotel para a disciplina de Fullstack I das Faculdades Integradas de Taquara.
# Time de devs -> Guilherme Staffen, Thauã Reichert, Rodrigo Machado
# fullstack1-hotel-manager


```mermaid
erDiagram
    FUNCIONARIO {
        int id_funcionario PK
        string nome
        string cargo
        string login
        string senha
        boolean ativo
    }

    QUARTO {
        int id_quarto PK
        int id_tipo_quarto FK
        string numero
        int capacidade
        int status FK
    }

    TIPO_QUARTO {
        int id_tipo_quarto PK
        string nome_tipo_quarto
    }

    TARIFA_TIPO_QUARTO {
        int id_tarifa_tipo_quarto PK
        int id_tipo_quarto FK
        string nome_tarifa_tipo_quarto
        date data_inicio_vigencia 
        date data_fim_vigencia 
    }

    STATUS_QUARTO {
        int id_status_quarto PK
        string nome_status_quarto
    }

    CLIENTE {
        int id_cliente PK
        string nome
        string documento
        string telefone
        string endereco
        boolean ativo
    }

    RESERVA {
        int id_reserva PK
        date data_reserva
        date data_check_in
        date data_check_out
        int id_cliente FK
        int id_funcionario FK
        int id_quarto FK
        int id_status_reserva FK
        int id_tarifa_tipo_quarto FK
    }

    STATUS_RESERVA {
        int id_status_reserva PK
        string nome_status_reserva
    }

    OCORRENCIA {
        int id_ocorrencia PK
        int id_quarto FK
        date data_abertura_ocorrencia
        date data_fechamento_concorrencia
        string descricao
        boolean finalizada
    }



    FUNCIONARIO }|--o{ RESERVA : "gerencia"
    CLIENTE ||--o{ RESERVA : "realiza"
    STATUS_RESERVA ||--o{ RESERVA : "associado a"
    OCORRENCIA }o--|| QUARTO : "associado a"
    
    
    QUARTO ||--o{ RESERVA : "associado a"
    QUARTO |o--|| STATUS_QUARTO: "tem"
    
    QUARTO |o--|| TIPO_QUARTO: "tem"
    TIPO_QUARTO ||--|{ TARIFA_TIPO_QUARTO: "tem"

    TARIFA_TIPO_QUARTO ||--o{ RESERVA: "associado a" 
```
