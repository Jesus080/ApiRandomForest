# 🏗️ Diagramas de Arquitectura

Diagramas visuales de la arquitectura del proyecto usando Mermaid.

## 📊 Arquitectura General

```mermaid
graph TB
    subgraph "Cliente"
        A[Usuario/App] --> B[HTTP Request]
    end
    
    subgraph "Render Cloud"
        B --> C[Gunicorn Server]
        C --> D[Django Application]
        
        subgraph "Django App"
            D --> E[URLs Router]
            E --> F[Views Layer]
            F --> G[Serializers]
            G --> H[Services Layer]
            H --> I[ML Model]
        end
        
        I --> J[(Random Forest<br/>79 features)]
    end
    
    J --> K[Prediction Result]
    K --> F
    F --> L[JSON Response]
    L --> A
    
    style A fill:#e1f5ff
    style J fill:#ffe1e1
    style D fill:#e1ffe1
```

## 🔄 Flujo de una Petición de Predicción

```mermaid
sequenceDiagram
    participant C as Cliente
    participant V as Views
    participant S as Serializer
    participant Svc as Service
    participant M as ML Model
    
    C->>V: POST /api/predict/
    activate V
    
    V->>S: Validar datos
    activate S
    S-->>V: Datos validados
    deactivate S
    
    V->>Svc: predict(features)
    activate Svc
    
    Svc->>Svc: _validate_features()
    Svc->>Svc: _prepare_input()
    
    Svc->>M: predict(data)
    activate M
    M-->>Svc: prediction + proba
    deactivate M
    
    Svc-->>V: result dict
    deactivate Svc
    
    V->>S: Serializar respuesta
    activate S
    S-->>V: JSON serializado
    deactivate S
    
    V-->>C: Response 200 OK
    deactivate V
```

## 🏛️ Arquitectura en Capas

```mermaid
graph TD
    subgraph "Presentation Layer"
        A[REST Endpoints<br/>views.py]
        B[HTML Interface<br/>templates/]
    end
    
    subgraph "Validation Layer"
        C[DRF Serializers<br/>serializers.py]
    end
    
    subgraph "Business Logic Layer"
        D[ML Service<br/>services.py]
    end
    
    subgraph "Data Layer"
        E[ML Models<br/>models/*.pkl]
    end
    
    A --> C
    B --> A
    C --> D
    D --> E
    
    style A fill:#ff9999
    style C fill:#99ff99
    style D fill:#9999ff
    style E fill:#ffff99
```

## 📁 Estructura de Archivos

```mermaid
graph TD
    Root[ApiRandomForest/]
    
    Root --> NB[Random_Forest.ipynb]
    Root --> DS[TotalFeatures.csv]
    
    Root --> MA[malware_api/]
    MA --> S[settings.py]
    MA --> U[urls.py]
    MA --> W[wsgi.py]
    
    Root --> PR[predictor/]
    PR --> SV[services.py<br/>⭐ ML Logic]
    PR --> VW[views.py<br/>⭐ Endpoints]
    PR --> SR[serializers.py<br/>⭐ Validation]
    PR --> UR[urls.py]
    
    Root --> MO[models/]
    MO --> RF[malware_detector_rf.pkl]
    MO --> FC[feature_columns.pkl]
    
    Root --> TE[templates/]
    TE --> HT[home.html]
    
    Root --> DO[📚 Docs/]
    DO --> RD[README.md]
    DO --> DP[DEPLOYMENT.md]
    DO --> CC[CLEAN_CODE.md]
    
    style SV fill:#ffcccc
    style VW fill:#ccffcc
    style SR fill:#ccccff
    style RF fill:#ffffcc
```

## 🔐 Patrón Singleton del Servicio ML

```mermaid
classDiagram
    class MalwareDetectorService {
        -_instance: MalwareDetectorService
        -_model: RandomForestClassifier
        -_feature_columns: List
        -_is_loaded: bool
        
        +__new__() MalwareDetectorService
        +load_model() void
        +predict(data) Dict
        -_validate_features(data) void
        -_prepare_input(data) DataFrame
        +get_model_info() Dict
        +is_ready: bool
    }
    
    note for MalwareDetectorService "Singleton Pattern\nSolo una instancia en memoria"
```

## 🌐 Endpoints y Métodos HTTP

```mermaid
graph LR
    A[API Root /api/] --> B[GET /]
    A --> C[GET /health/]
    A --> D[GET /model-info/]
    A --> E[GET /features/]
    A --> F[POST /predict/]
    
    B --> G[HTML Interface]
    C --> H[Health Status]
    D --> I[Model Details]
    E --> J[Features List]
    F --> K[Malware Prediction]
    
    style F fill:#ffcccc
    style B fill:#ccffcc
```

## 🔄 Ciclo de Vida del Request

```mermaid
stateDiagram-v2
    [*] --> ReceivedRequest
    ReceivedRequest --> URLRouting
    URLRouting --> ViewFunction
    ViewFunction --> InputValidation
    
    InputValidation --> ValidationError: Error
    ValidationError --> ErrorResponse
    
    InputValidation --> ServiceCall: OK
    ServiceCall --> ModelPrediction
    
    ModelPrediction --> PredictionError: Error
    PredictionError --> ErrorResponse
    
    ModelPrediction --> ResultSerialization: OK
    ResultSerialization --> SuccessResponse
    
    ErrorResponse --> [*]
    SuccessResponse --> [*]
```

## 🏗️ Stack Tecnológico

```mermaid
graph TB
    subgraph "Frontend"
        A[HTML5]
        B[CSS3]
        C[JavaScript]
    end
    
    subgraph "Backend Framework"
        D[Django 4.2]
        E[Django REST Framework 3.14]
    end
    
    subgraph "Machine Learning"
        F[scikit-learn 1.3]
        G[pandas 2.1]
        H[numpy 1.26]
    end
    
    subgraph "Server"
        I[Gunicorn]
        J[WhiteNoise]
    end
    
    subgraph "Platform"
        K[Python 3.12.3]
        L[Render Cloud]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    F --> H
    D --> I
    I --> J
    I --> K
    K --> L
```

## 📊 Flujo de Datos de ML

```mermaid
graph LR
    A[Raw Network<br/>Traffic Features] --> B[Feature<br/>Validation]
    B --> C[Data<br/>Preprocessing]
    C --> D[DataFrame<br/>Creation]
    D --> E[Random Forest<br/>Model]
    E --> F[Prediction]
    E --> G[Probabilities]
    F --> H[Label:<br/>malware/benign]
    G --> I[Confidence %]
    H --> J[JSON Response]
    I --> J
    
    style E fill:#ffcccc
    style J fill:#ccffcc
```

## 🔒 Seguridad y Validación

```mermaid
graph TD
    A[Client Request] --> B{Content-Type<br/>Valid?}
    B -->|No| C[400 Bad Request]
    B -->|Yes| D{Features<br/>Present?}
    
    D -->|No| C
    D -->|Yes| E{All 79<br/>Features?}
    
    E -->|No| C
    E -->|Yes| F{Numeric<br/>Values?}
    
    F -->|No| C
    F -->|Yes| G[Process Request]
    
    G --> H{Model<br/>Loaded?}
    H -->|No| I[500 Server Error]
    H -->|Yes| J[Make Prediction]
    
    J --> K{Success?}
    K -->|No| I
    K -->|Yes| L[200 OK Response]
```

## 🚀 Deployment Pipeline

```mermaid
graph LR
    A[Local Development] --> B[Git Commit]
    B --> C[Push to GitHub]
    C --> D[Render Webhook]
    D --> E[Build Phase]
    E --> F{Build<br/>Success?}
    
    F -->|No| G[Build Failed]
    F -->|Yes| H[Install Dependencies]
    H --> I[Collect Static Files]
    I --> J[Run Migrations]
    J --> K[Start Gunicorn]
    K --> L[Health Check]
    L --> M{Healthy?}
    
    M -->|No| N[Rollback]
    M -->|Yes| O[Deploy Live]
    
    style O fill:#ccffcc
    style G fill:#ffcccc
    style N fill:#ffcccc
```

## 💾 Modelo de Datos (Simplified)

```mermaid
erDiagram
    API ||--o{ REQUEST : receives
    REQUEST ||--|| FEATURES : contains
    FEATURES ||--|| VALIDATION : validated-by
    VALIDATION ||--|| SERVICE : processed-by
    SERVICE ||--|| MODEL : uses
    MODEL ||--|| PREDICTION : generates
    PREDICTION ||--|| RESPONSE : returns
    
    REQUEST {
        json body
        string method
        string path
    }
    
    FEATURES {
        float flow_duration
        float Header_Length
        float Protocol_Type
    }
    
    PREDICTION {
        int prediction
        string label
        array confidence
        float confidence_percentage
    }
```

---

## 📝 Cómo Ver los Diagramas

### En GitHub
Los diagramas Mermaid se renderizan automáticamente en GitHub.

### En VS Code
1. Instalar extensión: "Markdown Preview Mermaid Support"
2. Abrir este archivo
3. Presionar `Ctrl+Shift+V` (o `Cmd+Shift+V` en Mac)

### En Otros Editores
1. Copiar el código Mermaid
2. Pegar en [Mermaid Live Editor](https://mermaid.live/)
3. Ver el diagrama renderizado

---

**Estos diagramas te ayudan a entender visualmente la arquitectura del proyecto.** 🎨
