import os
from typing import List, Union, Optional

from fastapi import APIRouter, Body, HTTPException, Query

from boaviztapi import config, data_dir
from boaviztapi.dto.device import Server
from boaviztapi.dto.device.device import mapper_server
from boaviztapi.model.device import Device
from boaviztapi.model.device.server import DeviceServer
from boaviztapi.routers.openapi_doc.descriptions import server_impact_by_model_description, \
    server_impact_by_config_description, all_archetype_servers, get_archetype_config_desc
from boaviztapi.routers.openapi_doc.examples import server_configuration_examples_openapi
from boaviztapi.service.archetype import get_server_archetype, get_device_archetype_lst
from boaviztapi.service.verbose import verbose_device
from boaviztapi.service.impacts_computation import compute_impacts

# Hexagonal architecture imports
from boaviztapi.core.di_container import get_container
from boaviztapi.adapters.driving.rest.schemas.server import ServerRequestSchema
from boaviztapi.adapters.driving.rest.schemas.common import UsageSchema
from boaviztapi.adapters.driving.rest.mappers.server_mapper import ServerMapper
from boaviztapi.adapters.driving.rest.mappers.response_mapper import ResponseMapper
from boaviztapi.core.domain.model.usage import UsageConfiguration
from boaviztapi.core.domain.model.device import DeviceConfiguration

server_router = APIRouter(
    prefix='/v1/server',
    tags=['server']
)


@server_router.get('/archetypes',
                   description=all_archetype_servers)
async def server_get_all_archetype_name():
    return get_device_archetype_lst(os.path.join(data_dir, 'archetypes/server.csv'))


@server_router.get('/archetype_config',
                   description=get_archetype_config_desc)
async def get_archetype_config(archetype: str = Query(example=config["default_server"])):
    result = get_server_archetype(archetype)
    if not result:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")
    return result


@server_router.get('/',
                   description=server_impact_by_model_description)
async def server_impact_from_model(archetype: str = config["default_server"],
                                   verbose: bool = True,
                                   duration: Optional[float] = config["default_duration"],
                                   criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_server_archetype(archetype)

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    model_server = DeviceServer(archetype=archetype_config)

    return await server_impact(
        device=model_server,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@server_router.post('/',
                    description=server_impact_by_config_description)
async def server_impact_from_configuration(
        server: Server = Body(None, openapi_examples=server_configuration_examples_openapi),
        verbose: bool = True,
        duration: Optional[float] = config["default_duration"],
        archetype: str = config["default_server"],
        criteria: List[str] = Query(config["default_criteria"])):
    archetype_config = get_server_archetype(archetype)

    if not archetype_config:
        raise HTTPException(status_code=404, detail=f"{archetype} not found")

    completed_server = mapper_server(server, archetype=archetype_config)

    return await server_impact(
        device=completed_server,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


async def server_impact(device: Device,
                        verbose: bool,
                        duration: Optional[float] = config["default_duration"],
                        criteria: List[str] = Query(config["default_criteria"])) -> dict:
    if duration is None:
        duration = device.usage.hours_life_time.value

    impacts = compute_impacts(model=device, selected_criteria=criteria, duration=duration)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_device(device, selected_criteria=criteria, duration=duration)
        }
    return {"impacts": impacts}


# ============================================================================
# Hexagonal Architecture Endpoints (Phase 6)
# ============================================================================
# These endpoints demonstrate the new hexagonal architecture pattern.
# They will eventually replace the legacy endpoints above.


@server_router.post('/v2',
                    description="Compute server impact using hexagonal architecture (Phase 6)")
async def server_impact_v2(
        server: Optional[ServerRequestSchema] = Body(None),
        usage: Optional[UsageSchema] = Body(None),
        verbose: bool = True,
        duration: Optional[float] = None,
        criteria: List[str] = Query(default=["gwp", "pe", "adp"])):
    """
    Compute server environmental impact using the new hexagonal architecture.
    
    This endpoint uses:
    - Domain models (pure business logic)
    - Use cases (orchestration)
    - Driven adapters (data access)
    - Driving adapters (REST mapping)
    """
    # Get the use case from DI container
    container = get_container()
    use_case = container.get_compute_server_impact_use_case()
    
    # Map API request to domain models
    if server:
        device_config = ServerMapper.to_device_configuration(server)
    else:
        # Create minimal default configuration
        device_config = DeviceConfiguration(
            cpu=None,
            ram=None,
            disk=None,
            power_supply=None,
            case=None
        )
    
    # Map usage configuration
    if usage:
        usage_config = UsageSchema.to_domain(usage)
    else:
        # Use default usage from config
        from decimal import Decimal
        usage_config = UsageConfiguration(
            hours_use_time=Decimal("8760.0"),  # 1 year
            hours_life_time=Decimal("35040.0"),  # 4 years
            location=config.get("default_location", "EEE")
        )
    
    # Use default duration if not provided
    if duration is None:
        duration = 8760.0  # 1 year in hours
    
    # Execute use case
    try:
        impact_result = use_case.execute(
            device_config=device_config,
            usage_config=usage_config,
            criteria=criteria,
            duration=duration,
            verbose=verbose
        )
        
        # Map domain result to API response
        response = ResponseMapper.to_impact_response_schema(impact_result, verbose=verbose)
        
        return response.dict(exclude_none=True)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
