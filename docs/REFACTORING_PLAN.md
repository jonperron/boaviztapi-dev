# BoaviztAPI Refactoring Plan: Hexagonal Architecture

## Overview

This document outlines a comprehensive plan to refactor BoaviztAPI using **Hexagonal Architecture** (also known as Ports & Adapters) combined with principles from **Clean Architecture**.

### Goals

1. **Compute Engine**: Isolate the core business logic for computing environmental impacts
2. **API Layer**: Create a thin FastAPI adapter that exposes the compute engine
3. **Testability**: Enable testing of business logic without API dependencies
4. **Reusability**: Allow the compute engine to be used by CLI, batch jobs, or other interfaces

### Architecture Principles

This refactoring follows:

- **Hexagonal Architecture** (Alistair Cockburn): Ports & Adapters pattern
- **Clean Architecture** (Robert C. Martin): Dependency rule (dependencies point inward)
- **SOLID Principles**: Especially Dependency Inversion and Interface Segregation

---

## Hexagonal Architecture Overview

```
                         ┌─────────────────────────────────┐
                         │       DRIVING ADAPTERS          │
                         │      (Primary/Input)            │
                         │                                 │
                         │  ┌──────────┐   ┌──────────┐   │
                         │  │ REST API │   │   CLI    │   │
                         │  │ (FastAPI)│   │ (Future) │   │
                         │  └────┬─────┘   └────┬─────┘   │
                         │       │              │         │
                         └───────┼──────────────┼─────────┘
                                 │              │
                                 ▼              ▼
                         ┌─────────────────────────────────┐
                         │         INPUT PORTS             │
                         │        (Interfaces)             │
                         │                                 │
                         │  ┌──────────────────────────┐   │
                         │  │ IComputeServerImpact     │   │
                         │  │ IComputeCloudImpact      │   │
                         │  │ IComputeComponentImpact  │   │
                         │  └──────────────────────────┘   │
                         └───────────────┬─────────────────┘
                                         │
                                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION CORE                                  │
│                                                                            │
│   ┌────────────────────────────────────────────────────────────────────┐   │
│   │                        USE CASES                                   │   │
│   │                                                                    │   │
│   │  ┌─────────────────────┐  ┌─────────────────────┐                 │   │
│   │  │ ComputeServerImpact │  │ ComputeCloudImpact  │  ...            │   │
│   │  └──────────┬──────────┘  └──────────┬──────────┘                 │   │
│   │             │                        │                             │   │
│   └─────────────┼────────────────────────┼─────────────────────────────┘   │
│                 │                        │                                  │
│                 ▼                        ▼                                  │
│   ┌────────────────────────────────────────────────────────────────────┐   │
│   │                      DOMAIN MODEL                                  │   │
│   │                                                                    │   │
│   │  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐   │   │
│   │  │ DeviceConfig     │  │ UsageConfig      │  │ ImpactResult   │   │   │
│   │  │ CPUConfig        │  │ WorkloadProfile  │  │ ImpactValue    │   │   │
│   │  │ RAMConfig        │  │ ElecFactors      │  │ PhaseImpact    │   │   │
│   │  └──────────────────┘  └──────────────────┘  └────────────────┘   │   │
│   └────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
                         ┌─────────────────────────────────┐
                         │        OUTPUT PORTS             │
                         │       (Interfaces)              │
                         │                                 │
                         │  ┌──────────────────────────┐   │
                         │  │ IArchetypeRepository     │   │
                         │  │ IFactorProvider          │   │
                         │  │ IElectricalMixProvider   │   │
                         │  └──────────────────────────┘   │
                         └───────────────┬─────────────────┘
                                         │
                                         ▼
                         ┌─────────────────────────────────┐
                         │       DRIVEN ADAPTERS           │
                         │     (Secondary/Output)          │
                         │                                 │
                         │  ┌──────────┐   ┌──────────┐   │
                         │  │ CSV/YAML │   │ External │   │
                         │  │  Reader  │   │   API    │   │
                         │  └──────────┘   └──────────┘   │
                         └─────────────────────────────────┘
```

### Key Concepts

| Hexagonal Term | Description | Example in BoaviztAPI |
|----------------|-------------|----------------------|
| **Application Core** | Business logic, domain models, use cases | Impact computation logic |
| **Port** | Interface defining how to interact with the core | `IComputeServerImpact` |
| **Driving Adapter** | External actor that calls the core (input) | FastAPI REST endpoint |
| **Driven Adapter** | External service called by the core (output) | CSV archetype repository |
| **Use Case** | Single business operation | Compute server impact |
| **Domain Model** | Pure business entities (no framework dependencies) | `DeviceConfiguration` |

---

## Current State Analysis

### Current Structure
```
boaviztapi/
├── dto/                    # Data Transfer Objects (mixed concerns)
├── model/                  # Domain models (tightly coupled)
├── routers/                # API endpoints (business logic embedded)
├── service/                # Business services (API-aware)
└── utils/                  # Utilities
```

### Issues with Current Architecture

- DTOs are used across both API and compute layers
- Business logic is embedded in API routers
- Tight coupling between API schemas and domain models
- Difficult to test compute logic in isolation
- Cannot reuse compute engine for CLI or batch processing

### Specific Dependency Violations

#### 1. Domain Models Depend on Infrastructure

Domain models directly call archetype service in constructors:

```python
# model/component/cpu.py - CURRENT (VIOLATION)
class ComponentCPU(Component):
    def __init__(self, archetype=get_component_archetype(config["default_cpu"], "cpu")):
        # Domain depends on infrastructure (file I/O)
```

#### 2. Configuration Coupling

Domain models and services directly import the `config` dictionary:

```python
# Used throughout codebase - VIOLATION
from boaviztapi import config
default_duration = config["default_duration"]
```

#### 3. No Repository Abstraction

Data access is directly embedded in service functions:

```python
# service/archetype.py - CURRENT
def get_archetype(archetype_name: str, csv_path: str):
    with open(csv_path) as csvfile:  # Direct file I/O in service layer
        reader = csv.DictReader(csvfile)
```

### Current Architecture Strengths

Before refactoring, we should acknowledge what's already well-designed:

#### 1. Rich Domain Models

The `Boattribute` class is an excellent domain concept that:

- Tracks value provenance (INPUT, DEFAULT, ARCHETYPE, COMPLETED)
- Supports min/max ranges for uncertainty modeling
- Enables lazy completion through registered functions
- Maintains transparency about data sources

```python
class Boattribute:
    """Smart attribute with status tracking and lazy completion"""
    _value: Any
    _min: Any
    _max: Any
    status: Status  # NONE, INPUT, COMPLETED, DEFAULT, CHANGED, ARCHETYPE
    source: Optional[str]
    complete_function: Optional[Callable]
```

#### 2. DTO-Domain Separation

The codebase already has explicit mappers between DTOs and domain models:

```python
# DTO (API contract)
class CPU(ComponentDTO):
    core_units: Optional[int]

# Domain Model (business logic)
class ComponentCPU(Component):
    core_units: Boattribute

# Explicit mapper
def mapper_cpu(cpu_dto: CPU, archetype=...) -> ComponentCPU:
    cpu_component = ComponentCPU(archetype=archetype)
    if cpu_dto.core_units is not None:
        cpu_component.core_units.set_input(cpu_dto.core_units)
    return cpu_component
```

#### 3. Configuration Externalization

- YAML-based configuration (`config.yml`, `factors.yml`)
- Data-driven archetype system (CSV files)
- No hardcoded values in business logic

#### 4. Good Test Structure

- Unit tests target domain logic
- Integration tests verify API behavior
- Test data is isolated from production data

---

## Target Architecture (Hexagonal)

### Proposed Structure

```text
boaviztapi/
├── adapters/                       # HEXAGONAL: All Adapters
│   ├── driving/                    # Primary Adapters (Input)
│   │   ├── rest/                   # FastAPI REST API
│   │   │   ├── routers/           # API endpoints
│   │   │   ├── schemas/           # Pydantic request/response models
│   │   │   ├── mappers/           # API ↔ Domain mappers
│   │   │   └── dependencies/      # FastAPI dependencies
│   │   └── cli/                    # (Future) Command-line interface
│   │
│   └── driven/                     # Secondary Adapters (Output)
│       ├── persistence/            # Data access implementations
│       │   ├── archetype_repo.py  # CSV/YAML archetype loading
│       │   └── factor_repo.py     # Impact factors loading
│       └── external/               # (Future) External API clients
│
├── core/                           # HEXAGONAL: Application Core
│   ├── domain/                     # Enterprise Business Rules
│   │   ├── model/                 # Domain entities (dataclasses)
│   │   │   ├── device.py         # DeviceConfiguration, CPUConfig, etc.
│   │   │   ├── usage.py          # UsageConfiguration, WorkloadProfile
│   │   │   └── result.py         # ImpactResult, ImpactValue
│   │   └── service/               # Domain services
│   │       └── impact_calculator.py  # Pure computation logic
│   │
│   ├── ports/                      # HEXAGONAL: Port Interfaces
│   │   ├── input/                 # Driving Ports (called by adapters)
│   │   │   ├── compute_server.py # IComputeServerImpact
│   │   │   ├── compute_cloud.py  # IComputeCloudImpact
│   │   │   └── compute_component.py
│   │   └── output/                # Driven Ports (implemented by adapters)
│   │       ├── archetype_repo.py # IArchetypeRepository
│   │       └── factor_provider.py # IFactorProvider
│   │
│   └── use_cases/                  # Application Business Rules
│       ├── compute_server_impact.py
│       ├── compute_cloud_impact.py
│       └── compute_component_impact.py
│
├── shared/                         # Cross-cutting concerns
│   ├── config/                    # Configuration loading
│   ├── container/                 # Dependency Injection container
│   ├── exceptions/                # Common exceptions
│   └── utils/                     # Common utilities
│
└── tests/
    ├── unit/
    │   ├── core/                  # Core logic tests (no adapters)
    │   └── adapters/              # Adapter-specific tests
    ├── integration/               # Integration tests
    └── e2e/                       # End-to-end API tests
```

### Dependency Flow (Clean Architecture)
```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                 │
│  │ Routers │───>│ Schemas │───>│ Mappers │                 │
│  └────┬────┘    └─────────┘    └────┬────┘                 │
│       │                              │                      │
└───────┼──────────────────────────────┼──────────────────────┘
        │                              │
        ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Core Layer                            │
│  ┌────────────┐    ┌──────────┐    ┌────────────┐          │
│  │ Interfaces │<───│ Services │───>│ Repository │          │
│  └────────────┘    └────┬─────┘    └────────────┘          │
│                         │                                   │
│                         ▼                                   │
│                   ┌──────────┐                              │
│                   │  Models  │                              │
│                   └──────────┘                              │
└─────────────────────────────────────────────────────────────┘
        │                              │
        ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Shared Layer                           │
│  ┌────────┐    ┌───────────┐    ┌────────────┐             │
│  │ Config │    │ Container │    │ Exceptions │             │
│  └────────┘    └───────────┘    └────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Analysis & Port Definition (Week 1-2)

#### 1.1 Dependency Mapping

**Tasks:**

- [ ] Map all imports between `routers/` and `service/`
- [ ] Map all imports between `dto/` and `model/`
- [ ] Identify shared state and global variables
- [ ] Document current data flow for each endpoint

**Deliverables:**

- Dependency graph diagram
- Data flow documentation
- List of coupling points

#### 1.2 Port Interface Definition (Hexagonal)

**Tasks:**

- [ ] Define Input Ports (driving): `IComputeServerImpact`, `IComputeCloudImpact`
- [ ] Define Output Ports (driven): `IArchetypeRepository`, `IFactorProvider`
- [ ] Define domain result models

**Deliverables:**

- Port interfaces in `core/ports/input/` and `core/ports/output/`
- Domain model definitions in `core/domain/model/`

---

### Phase 2: Create Domain Layer (Week 3-4)

#### 2.1 Domain Models (Enterprise Business Rules)

**Tasks:**

- [ ] Create `DeviceConfiguration` dataclass
- [ ] Create `UsageConfiguration` dataclass
- [ ] Create `ImpactResult` dataclass
- [ ] Create component configuration dataclasses

**Key Principle:** Domain models must have NO dependencies on Pydantic, FastAPI, or any framework.

```python
# core/domain/model/device.py
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class DeviceConfiguration:
    """Pure domain model - no framework dependencies"""
    cpu: Optional['CPUConfiguration'] = None
    ram: List['RAMConfiguration'] = None
    disk: List['DiskConfiguration'] = None
```

#### 2.2 Input Port Interfaces

```python
# core/ports/input/compute_server.py
from abc import ABC, abstractmethod
from core.domain.model.device import DeviceConfiguration
from core.domain.model.usage import UsageConfiguration
from core.domain.model.result import ImpactResult

class IComputeServerImpact(ABC):
    """Input Port: Driving adapter calls this interface"""
    
    @abstractmethod
    def execute(
        self,
        device_config: DeviceConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: float
    ) -> ImpactResult:
        pass
```

#### 2.3 Output Port Interfaces

```python
# core/ports/output/archetype_repository.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IArchetypeRepository(ABC):
    """Output Port: Core uses this, Driven adapter implements this"""
    
    @abstractmethod
    def get_server_archetype(self, archetype_id: str) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_cloud_instance_archetype(
        self, 
        instance_type: str, 
        provider: str
    ) -> Optional[Dict[str, Any]]:
        pass
```

---

### Phase 3: Implement Driving Adapters (Week 5-6)

#### 3.1 API Mappers (Adapter Layer)

**Tasks:**

- [ ] Create `ServerMapper` (API Schema → Domain Model)
- [ ] Create `CloudMapper` (API Schema → Domain Model)
- [ ] Create `ResponseMapper` (Domain Model → API Schema)

```python
# adapters/driving/rest/mappers/server_mapper.py
from adapters.driving.rest.schemas.server import ServerRequest
from core.domain.model.device import DeviceConfiguration

class ServerMapper:
    """Adapter: Maps REST API schemas to Domain models"""
    
    @staticmethod
    def to_device_config(request: ServerRequest) -> DeviceConfiguration:
        """Convert API request to domain model"""
        pass
    
    @staticmethod
    def to_usage_config(request: ServerRequest) -> UsageConfiguration:
        """Convert API usage to domain model"""
        pass
```

#### 3.2 API Schemas (Pydantic)

```python
# adapters/driving/rest/schemas/server.py
from pydantic import BaseModel
from typing import Optional, Dict, Any

class ServerRequest(BaseModel):
    """REST API request schema - separate from domain"""
    model: Optional[Dict[str, Any]] = None
    configuration: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, Any]] = None
```

---

### Phase 4: Implement Use Cases (Week 7-8)

#### 4.1 Use Case Implementation

**Tasks:**

- [ ] Create `ComputeServerImpactUseCase` class
- [ ] Migrate computation logic from current services
- [ ] Use Output Ports for data access (not concrete implementations)
- [ ] Implement proper error handling

```python
# core/use_cases/compute_server_impact.py
from core.ports.input.compute_server import IComputeServerImpact
from core.ports.output.archetype_repository import IArchetypeRepository
from core.ports.output.factor_provider import IFactorProvider
from core.domain.model.device import DeviceConfiguration
from core.domain.model.result import ImpactResult

class ComputeServerImpactUseCase(IComputeServerImpact):
    """Use Case: Implements Input Port, uses Output Ports"""
    
    def __init__(
        self,
        archetype_repo: IArchetypeRepository,  # Output Port
        factor_provider: IFactorProvider       # Output Port
    ):
        self._archetype_repo = archetype_repo
        self._factor_provider = factor_provider
    
    def execute(
        self,
        device_config: DeviceConfiguration,
        usage_config: UsageConfiguration,
        criteria: List[str],
        duration: float
    ) -> ImpactResult:
        """Execute the use case - pure business logic"""
        # Get archetype defaults
        archetype = self._archetype_repo.get_server_archetype("DEFAULT")
        
        # Get electrical factors
        factors = self._factor_provider.get_electrical_factors(usage_config.location)
        
        # Compute impacts (business logic)
        manufacture_impact = self._compute_manufacture(device_config, criteria)
        use_impact = self._compute_use(device_config, usage_config, factors, duration)
        
        return ImpactResult(manufacture=manufacture_impact, use=use_impact)
```

---

### Phase 5: Implement Driven Adapters (Week 9-10)

#### 5.1 Persistence Adapters

**Tasks:**

- [ ] Create `ArchetypeRepository` (implements `IArchetypeRepository`)
- [ ] Create `FactorProvider` (implements `IFactorProvider`)
- [ ] Migrate data loading logic
- [ ] Copy existing component tests from the API layer and adapt them to test new API schemas
- [ ] Ensure new schemas produce identical responses to existing API endpoints for validation

```python
# adapters/driven/persistence/archetype_repository.py
from core.ports.output.archetype_repository import IArchetypeRepository
import pandas as pd

class ArchetypeRepository(IArchetypeRepository):
    """Driven Adapter: Implements Output Port for CSV/YAML data"""
    
    def __init__(self, data_path: str):
        self._data_path = data_path
        self._cache = {}
    
    def get_server_archetype(self, archetype_id: str) -> Optional[Dict[str, Any]]:
        """Load archetype from CSV file"""
        if archetype_id not in self._cache:
            df = pd.read_csv(f"{self._data_path}/archetypes/server.csv")
            self._cache[archetype_id] = df[df['id'] == archetype_id].to_dict()
        return self._cache.get(archetype_id)
```

#### 5.2 Dependency Injection Container

**Tasks:**

- [ ] Add `dependency-injector` package
- [ ] Create container configuration
- [ ] Wire up Use Cases with Adapters

```python
# shared/container/container.py
from dependency_injector import containers, providers
from core.use_cases.compute_server_impact import ComputeServerImpactUseCase
from adapters.driven.persistence.archetype_repository import ArchetypeRepository
from adapters.driven.persistence.factor_provider import FactorProvider

class Container(containers.DeclarativeContainer):
    """DI Container: Wires Adapters to Ports"""
    
    config = providers.Configuration()
    
    # Driven Adapters (implement Output Ports)
    archetype_repository = providers.Singleton(
        ArchetypeRepository,
        data_path=config.data_path
    )
    
    factor_provider = providers.Singleton(
        FactorProvider,
        data_path=config.data_path
    )
    
    # Use Cases (implement Input Ports)
    compute_server_use_case = providers.Factory(
        ComputeServerImpactUseCase,
        archetype_repo=archetype_repository,
        factor_provider=factor_provider
    )
```

---

### Phase 6: Wire Up REST Adapter (Week 11-12)

#### 6.1 Thin Router Layer (Driving Adapter)

**Tasks:**

- [ ] Refactor each router to use mappers and use cases
- [ ] Remove business logic from routers
- [ ] Add proper dependency injection
- [ ] Update tests

```python
# adapters/driving/rest/routers/server_router.py
from fastapi import APIRouter, Depends, Query
from adapters.driving.rest.schemas.server import ServerRequest, ImpactResponse
from adapters.driving.rest.mappers.server_mapper import ServerMapper, ResponseMapper
from core.ports.input.compute_server import IComputeServerImpact

router = APIRouter()

def get_compute_server_use_case(request: Request) -> IComputeServerImpact:
    """Dependency injection for use case"""
    return request.app.state.container.compute_server_use_case()

@router.post("/server", response_model=ImpactResponse)
async def compute_server_impact(
    request: ServerRequest,
    verbose: bool = Query(False),
    duration: float = Query(8760),
    criteria: List[str] = Query(["gwp", "adp", "pe"]),
    use_case: IComputeServerImpact = Depends(get_compute_server_use_case)
):
    """
    REST Endpoint (Driving Adapter)
    
    1. Receives HTTP request
    2. Maps to domain models
    3. Calls use case (Input Port)
    4. Maps result to HTTP response
    """
    # Map API → Domain
    device_config = ServerMapper.to_device_config(request)
    usage_config = ServerMapper.to_usage_config(request.usage)
    
    # Execute use case
    result = use_case.execute(
        device_config=device_config,
        usage_config=usage_config,
        criteria=criteria,
        duration=duration
    )
    
    # Map Domain → API
    return ResponseMapper.to_impact_response(result, verbose=verbose)
```

---

## Additional Patterns & Components

### Domain Exception Hierarchy

Create domain-specific exceptions to decouple error handling from HTTP concepts:

```python
# core/domain/exceptions.py

class DomainException(Exception):
    """Base exception for domain errors"""
    pass


class ArchetypeNotFoundError(DomainException):
    """Raised when an archetype doesn't exist"""
    def __init__(self, archetype_name: str, archetype_type: str):
        self.archetype_name = archetype_name
        self.archetype_type = archetype_type
        super().__init__(f"Archetype '{archetype_name}' not found for type '{archetype_type}'")


class InvalidComponentConfigurationError(DomainException):
    """Raised when component configuration is invalid"""
    def __init__(self, component_type: str, reason: str):
        self.component_type = component_type
        self.reason = reason
        super().__init__(f"Invalid {component_type} configuration: {reason}")


class ImpactComputationError(DomainException):
    """Raised when impact computation fails"""
    def __init__(self, phase: str, criteria: str, reason: str):
        self.phase = phase
        self.criteria = criteria
        super().__init__(f"Failed to compute {criteria} for {phase}: {reason}")


class CountryNotSupportedError(DomainException):
    """Raised when a country's impact factors are not available"""
    def __init__(self, country: str):
        self.country = country
        super().__init__(f"Impact factors not available for country: {country}")
```

Map domain exceptions to HTTP responses in the driving adapter:

```python
# adapters/driving/rest/error_handlers.py
from fastapi import Request
from fastapi.responses import JSONResponse
from core.domain.exceptions import (
    ArchetypeNotFoundError,
    InvalidComponentConfigurationError,
    DomainException
)

async def domain_exception_handler(request: Request, exc: DomainException):
    """Map domain exceptions to HTTP responses"""
    status_code = 500

    if isinstance(exc, ArchetypeNotFoundError):
        status_code = 404
    elif isinstance(exc, InvalidComponentConfigurationError):
        status_code = 400
    elif isinstance(exc, CountryNotSupportedError):
        status_code = 400

    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
            "details": getattr(exc, '__dict__', {})
        }
    )

# Register in main.py
app.add_exception_handler(DomainException, domain_exception_handler)
```

---

### Use Case Input/Output Contracts

Define explicit input/output dataclasses for each use case to make contracts clear:

```python
# core/use_cases/compute_server_impact.py
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class ComputeServerImpactInput:
    """Input contract for server impact computation"""
    server_config: Dict[str, Any]
    archetype: Optional[str] = None
    duration: float = 8760.0  # hours
    criteria: List[str] = None
    verbose: bool = True

    def __post_init__(self):
        if self.criteria is None:
            self.criteria = ["gwp", "adp", "pe"]


@dataclass
class ComputeServerImpactOutput:
    """Output contract for server impact computation"""
    impacts: Dict[str, Dict[str, Dict[str, float]]]
    verbose_data: Optional[Dict[str, Any]] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class ComputeServerImpactUseCase(IComputeServerImpact):
    """Use case with explicit input/output contracts"""
    
    def execute(self, input: ComputeServerImpactInput) -> ComputeServerImpactOutput:
        # Implementation...
        pass
```

**Benefits:**

- Clear, documented API for each use case
- Easy to validate inputs
- Self-documenting code
- IDE autocomplete support

---

### Component Factory Pattern

Remove archetype loading from domain model constructors by using factories:

```python
# BEFORE (current) - Domain depends on infrastructure
class ComponentCPU(Component):
    def __init__(self, archetype=get_component_archetype(config["default_cpu"], "cpu")):
        super().__init__(archetype=archetype)

# AFTER (refactored) - Pure domain model
class ComponentCPU(Component):
    def __init__(self, archetype: Optional[Dict[str, Any]] = None):
        super().__init__(archetype=archetype)
```

Create a factory in the application layer:

```python
# core/use_cases/factories/component_factory.py
from core.ports.output.archetype_repository import IArchetypeRepository
from core.domain.model.component import ComponentCPU, ComponentRAM, ComponentSSD

class ComponentFactory:
    """Factory for creating components with archetype data"""
    
    def __init__(self, archetype_repo: IArchetypeRepository):
        self._repo = archetype_repo

    def create_cpu(self, archetype_name: Optional[str] = None) -> ComponentCPU:
        archetype = None
        if archetype_name:
            archetype = self._repo.get_component_archetype(archetype_name, "cpu")
        return ComponentCPU(archetype=archetype)

    def create_ram(self, archetype_name: Optional[str] = None) -> ComponentRAM:
        archetype = None
        if archetype_name:
            archetype = self._repo.get_component_archetype(archetype_name, "ram")
        return ComponentRAM(archetype=archetype)

    # ... etc for other components
```

**Benefits:**

- Domain models become pure (no I/O in constructors)
- Easier to test models in isolation
- Clear separation of creation and business logic
- No default arguments that trigger file I/O

---

### Configuration Service (Output Port)

Create a typed configuration service instead of directly using the `config` dictionary:

```python
# core/ports/output/configuration.py
from abc import ABC, abstractmethod
from typing import List

class IConfiguration(ABC):
    """Output Port for application configuration"""

    @property
    @abstractmethod
    def default_duration(self) -> float:
        pass

    @property
    @abstractmethod
    def default_criteria(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def default_cpu_archetype(self) -> str:
        pass

    @property
    @abstractmethod
    def default_location(self) -> str:
        pass

    @property
    @abstractmethod
    def max_significant_figures(self) -> int:
        pass

    @property
    @abstractmethod
    def uncertainty_percentage(self) -> int:
        pass
```

```python
# adapters/driven/configuration/yaml_configuration.py
from core.ports.output.configuration import IConfiguration

class YamlConfiguration(IConfiguration):
    """Driven Adapter: YAML-based configuration"""
    
    def __init__(self, config_dict: dict):
        self._config = config_dict

    @property
    def default_duration(self) -> float:
        return float(self._config.get("default_duration") or 8760)

    @property
    def default_criteria(self) -> List[str]:
        return self._config.get("default_criteria", ["gwp", "adp", "pe"])

    @property
    def default_location(self) -> str:
        return self._config.get("default_location", "EEE")

    @property
    def max_significant_figures(self) -> int:
        return int(self._config.get("max_sig_fig", 4))

    @property
    def uncertainty_percentage(self) -> int:
        return int(self._config.get("uncertainty", 10))
```

**Benefits:**

- Type-safe configuration access
- No magic string keys
- IDE autocomplete support
- Easy to validate configuration at startup
- Testable with mock configurations

---

## Deployment Safety: Keeping Main Deployable

### ✅ YES, This Can Be Done Without Breaking the Project

The key is to use the **Strangler Fig Pattern** - incrementally replacing functionality while keeping the old code working.

### Strategy: Parallel Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                    TRANSITION PERIOD                        │
│                                                             │
│   ┌───────────────┐              ┌───────────────┐         │
│   │   OLD CODE    │              │   NEW CODE    │         │
│   │  (working)    │   migrate    │  (in progress)│         │
│   │               │  ─────────>  │               │         │
│   │  routers/     │              │  api/routers/ │         │
│   │  dto/         │              │  api/schemas/ │         │
│   │  service/     │              │  core/service/│         │
│   │  model/       │              │  core/model/  │         │
│   └───────────────┘              └───────────────┘         │
│          │                              │                   │
│          │    Both coexist until       │                   │
│          │    new code is validated    │                   │
│          ▼                              ▼                   │
│   ┌─────────────────────────────────────────────┐          │
│   │              SINGLE ENTRYPOINT              │          │
│   │                  main.py                    │          │
│   │         (routes to old OR new code)         │          │
│   └─────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Rules for Safe Migration

#### Rule 1: Parallel Implementation (During Migration)
```python
# main.py
from shared.config.feature_flags import FEATURE_FLAGS

if FEATURE_FLAGS["use_new_server_router"]:
    from api.routers.server_router import router as server_router
else:
    from boaviztapi.routers.server_router import server  # Old router

app.include_router(server_router, prefix="/v1/server")
```

#### Rule 2: Shadow Testing
- Run both old and new implementations in parallel
- Compare outputs for discrepancies
- Log differences without affecting users

```python
async def shadow_test_endpoint(request, old_result):
    """Compare new implementation against old (non-blocking)"""
    try:
        new_result = await new_compute_service.compute(...)
        if new_result != old_result:
            logger.warning(f"Shadow test mismatch: {diff(old_result, new_result)}")
    except Exception as e:
        logger.error(f"Shadow test failed: {e}")
    
    return old_result  # Always return old result during testing
```

#### Rule 3: Incremental Migration Order

| Order | Component | Risk Level | Rollback Complexity |
|-------|-----------|------------|---------------------|
| 1 | Core domain models | Low | Easy (additive) |
| 2 | Interfaces | Low | Easy (additive) |
| 3 | Mappers | Low | Easy (additive) |
| 4 | Core services | Medium | Moderate |
| 5 | API schemas | Medium | Moderate |
| 6 | Routers | High | Direct replacement |
| 7 | Remove old code | High | Git revert |

#### Rule 4: PR Strategy

Each PR should be:
- **Small**: Max 300-500 lines changed
- **Focused**: One component at a time
- **Tested**: All existing tests must pass
- **Backward compatible**: Old functionality still works

```
PR 1: Add core/model/device.py (additive, no breaking changes)
PR 2: Add core/model/usage.py (additive, no breaking changes)
PR 3: Add core/model/result.py (additive, no breaking changes)
PR 4: Add core/interfaces/ (additive, no breaking changes)
PR 5: Add api/mappers/ (additive, no breaking changes)
PR 6: Add core/service/ with feature flag (disabled by default)
PR 7: Add api/schemas/ (additive, no breaking changes)
PR 8: Refactor server_router with feature flag (disabled by default)
... enable feature flags one by one after validation ...
PR N: Remove old code (only after all flags enabled in production)
```

### CI/CD Safety Checks

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    steps:
      - name: Run all tests
        run: poetry run pytest
      
      - name: Check backward compatibility
        run: poetry run pytest tests/api/ -v
      
      - name: Validate API schema unchanged
        run: |
          poetry run python -c "from boaviztapi.main import app; import json; print(json.dumps(app.openapi()))" > new_schema.json
          diff expected_schema.json new_schema.json
```

### Rollback Plan

If something goes wrong at any phase:

1. **Git Revert** (Minutes)
   ```bash
   git revert <commit-hash>
   git push
   ```

2. **Full Rollback** (Last resort)
   ```bash
   git checkout <last-known-good-tag>
   git push --force
   ```

---

## Testing Strategy (Hexagonal)

### Test Pyramid

```text
                    ┌───────────┐
                    │   E2E     │  (Few, slow, high confidence)
                   ─┴───────────┴─
                  ┌───────────────┐
                  │  Integration  │  (Some, medium speed)
                 ─┴───────────────┴─
                ┌───────────────────┐
                │    Unit Tests     │  (Many, fast, focused)
               ─┴───────────────────┴─
```

### Core Unit Tests (No Adapters)

Test the Application Core in isolation by mocking Output Ports:

```python
# tests/unit/core/use_cases/test_compute_server_impact.py
import pytest
from unittest.mock import Mock
from core.use_cases.compute_server_impact import ComputeServerImpactUseCase
from core.domain.model.device import DeviceConfiguration, CPUConfiguration
from core.domain.model.usage import UsageConfiguration

@pytest.fixture
def mock_archetype_repo():
    """Mock Output Port"""
    repo = Mock()
    repo.get_server_archetype.return_value = {"CPU": {"units": 1}}
    return repo

@pytest.fixture
def mock_factor_provider():
    """Mock Output Port"""
    provider = Mock()
    provider.get_electrical_factors.return_value = {
        "gwp": {"value": 0.1, "min": 0.05, "max": 0.15}
    }
    return provider

def test_compute_server_impact_use_case(mock_archetype_repo, mock_factor_provider):
    """Test Use Case with mocked Output Ports - no adapters needed"""
    use_case = ComputeServerImpactUseCase(
        archetype_repo=mock_archetype_repo,
        factor_provider=mock_factor_provider
    )
    
    device_config = DeviceConfiguration(cpu=CPUConfiguration(units=2))
    usage_config = UsageConfiguration(location="FRA")
    
    result = use_case.execute(
        device_config=device_config,
        usage_config=usage_config,
        criteria=["gwp"],
        duration=8760
    )
    
    assert result is not None
    assert result.manufacture is not None
    assert "gwp" in result.manufacture.impacts
```

### Adapter Integration Tests

Test Driving Adapters (REST API) with mocked Use Cases:

```python
# tests/integration/adapters/driving/rest/test_server_endpoint.py
from fastapi.testclient import TestClient
from unittest.mock import Mock
from adapters.driving.rest.main import create_app
from core.domain.model.result import ImpactResult

def test_server_endpoint_calls_use_case():
    """Test Driving Adapter with mocked Use Case"""
    app = create_app()
    
    # Mock the Use Case (Input Port implementation)
    mock_use_case = Mock()
    mock_use_case.execute.return_value = ImpactResult(...)
    app.state.container.compute_server_use_case.override(lambda: mock_use_case)
    
    client = TestClient(app)
    
    response = client.post("/v1/server", json={
        "configuration": {"cpu": {"units": 2}},
        "usage": {"usage_location": "FRA"}
    })
    
    assert response.status_code == 200
    mock_use_case.execute.assert_called_once()
```

### E2E Tests (Full Stack)

Test the entire hexagon with real adapters:

```python
# tests/e2e/test_server_full_stack.py
def test_server_endpoint_e2e():
    """Test full hexagon: Driving Adapter → Use Case → Driven Adapter"""
    app = create_app()  # Real container with real adapters
    client = TestClient(app)
    
    response = client.post("/v1/server", json={
        "configuration": {"cpu": {"units": 2}},
        "usage": {"usage_location": "FRA"}
    })
    
    assert response.status_code == 200
    assert "impacts" in response.json()
    assert "gwp" in response.json()["impacts"]
```

---

## Timeline Summary

| Phase | Duration | Hexagonal Component | Risk to Production |
|-------|----------|---------------------|-------------------|
| 1. Analysis | 2 weeks | Port definitions | None |
| 2. Domain | 2 weeks | Domain models | None (additive) |
| 3. Driving Adapters | 2 weeks | REST mappers/schemas | None (additive) |
| 4. Use Cases | 2 weeks | Core business logic | None (additive) |
| 5. Driven Adapters | 2 weeks | Repository implementations | None (additive) |
| 6. Wire Up | 2 weeks | DI container, routers | Low (incremental) |
| 7. Cleanup | 2 weeks | Remove old code | Medium (after validation) |

**Total: ~14 weeks (3.5 months)**

---

## Benefits After Refactoring

### For Developers

- ✅ Clear hexagonal boundaries
- ✅ Easier to understand codebase
- ✅ Faster unit tests (no adapter overhead)
- ✅ Better IDE support and autocomplete

### For Testing

- ✅ Core logic testable by mocking Output Ports
- ✅ Adapters testable by mocking Input Ports
- ✅ Faster test execution
- ✅ Better test coverage

### For Reusability

- ✅ Compute engine usable via CLI (new Driving Adapter)
- ✅ Batch processing support
- ✅ Easy to add GraphQL/gRPC (new Driving Adapters)
- ✅ Library distribution possible (just the core)

### For Maintenance

- ✅ Changes to adapters don't affect core logic
- ✅ Changes to core don't require adapter updates
- ✅ Easier onboarding for new developers
- ✅ Reduced bug surface area

---

## Hexagonal Architecture Summary

```text
┌──────────────────────────────────────────────────────────────────┐
│                    DRIVING ADAPTERS (Primary)                    │
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   REST API      │  │      CLI        │  │   GraphQL       │  │
│  │   (FastAPI)     │  │   (Future)      │  │   (Future)      │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
└───────────┼────────────────────┼────────────────────┼───────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                        INPUT PORTS                               │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  IComputeServerImpact  │  IComputeCloudImpact  │  ...      │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                      APPLICATION CORE                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                      USE CASES                             │  │
│  │  ComputeServerImpactUseCase  │  ComputeCloudImpactUseCase  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                │                                 │
│                                ▼                                 │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    DOMAIN MODEL                            │  │
│  │  DeviceConfiguration  │  UsageConfiguration  │  ImpactResult │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                       OUTPUT PORTS                               │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  IArchetypeRepository  │  IFactorProvider  │  ...          │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬──────────────────────────────────┘
            │                    │                    │
            ▼                    ▼                    ▼
┌───────────┼────────────────────┼────────────────────┼───────────┐
│           │                    │                    │           │
│  ┌────────┴────────┐  ┌────────┴────────┐  ┌────────┴────────┐  │
│  │  CSV/YAML       │  │  External API   │  │   Database      │  │
│  │  Repository     │  │   (Future)      │  │   (Future)      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                  │
│                    DRIVEN ADAPTERS (Secondary)                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Key Metrics & Success Criteria

### Dependency Analysis

#### Current Module Dependencies (Before Refactoring)

```text
main.py
└── routers/* (8 modules)
    ├── dto/*
    │   └── pydantic (external)
    ├── service/impacts_computation.py
    │   ├── model/*
    │   ├── service/archetype.py
    │   │   └── data/*.csv (file I/O)
    │   └── service/factor_provider.py
    │       └── data/*.yml (file I/O)
    └── model/*
        ├── service/archetype.py  # VIOLATION: domain depends on infra
        └── __init__.py (config)   # VIOLATION: domain depends on config
```

#### Target Dependencies (After Refactoring)

```text
main.py
└── shared/container.py
    └── Creates all dependencies

adapters/driving/rest/routers/*
├── adapters/driving/rest/schemas/*
├── core/use_cases/*
│   ├── core/domain/model/*
│   ├── core/ports/input/* (interfaces)
│   └── core/ports/output/* (interfaces)
└── adapters/driving/rest/mappers/*

adapters/driven/persistence/*
└── core/ports/output/* (implements interfaces)

core/domain/*
└── No external dependencies (pure business logic)
```

### Measurable Goals

| Metric | Current | Target | How to Measure |
|--------|---------|--------|----------------|
| Domain layer external dependencies | 2 (service, config) | 0 | Count imports in `core/domain/` |
| Output Port abstractions (interfaces) | 0 | 3+ | Count ABC classes in `core/ports/output/` |
| Input Port abstractions (interfaces) | 0 | 3+ | Count ABC classes in `core/ports/input/` |
| Explicit use cases | 0 | 4-6 | Count use case classes |
| Domain exceptions | 0 | 5+ | Count exception classes |
| Unit test execution time | ~80s | <30s | `time poetry run pytest tests/unit/` |
| Core tests without I/O | ~20% | 80%+ | Tests that don't touch filesystem |

### Architecture Compliance Checks

Add automated checks to CI/CD:

```python
# scripts/check_architecture.py
"""Verify hexagonal architecture rules are followed"""

import ast
import os
from pathlib import Path

FORBIDDEN_IMPORTS = {
    "core/domain": ["fastapi", "pydantic", "pandas", "csv", "yaml"],
    "core/ports": ["fastapi", "pydantic", "pandas"],
    "core/use_cases": ["fastapi", "pydantic"],
}

def check_imports(directory: str, forbidden: list[str]) -> list[str]:
    """Check that a directory doesn't import forbidden modules"""
    violations = []
    for py_file in Path(directory).rglob("*.py"):
        with open(py_file) as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(alias.name.startswith(f) for f in forbidden):
                        violations.append(f"{py_file}: imports {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module and any(node.module.startswith(f) for f in forbidden):
                    violations.append(f"{py_file}: imports from {node.module}")
    return violations

def main():
    all_violations = []
    for directory, forbidden in FORBIDDEN_IMPORTS.items():
        if os.path.exists(directory):
            violations = check_imports(directory, forbidden)
            all_violations.extend(violations)
    
    if all_violations:
        print("Architecture violations found:")
        for v in all_violations:
            print(f"  - {v}")
        exit(1)
    else:
        print("✅ Architecture rules verified")
        exit(0)

if __name__ == "__main__":
    main()
```

```yaml
# Add to .github/workflows/ci.yml
- name: Check architecture compliance
  run: python scripts/check_architecture.py
```

---

## Conclusion

This refactoring plan uses **Hexagonal Architecture** to create a clear separation between:

1. **Application Core**: Pure business logic with no framework dependencies
2. **Ports**: Interfaces that define how the core communicates with the outside world
3. **Adapters**: Implementations that connect the core to specific technologies

The plan can be executed **safely without breaking main** by:

1. **Making additive changes first** (no deletions until validated)
2. **Running old and new code in parallel** during transition
3. **Migrating one component at a time** with thorough testing
4. **Keeping all existing tests passing** throughout
5. **Using incremental replacement** of routers after validation

The key insight is that we're not doing a "big bang" rewrite - we're incrementally building the hexagonal structure around the existing code, then migrating functionality piece by piece while maintaining full backward compatibility at every step.
