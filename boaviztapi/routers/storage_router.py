from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Query

from boaviztapi import config
from boaviztapi.compute.impacts_computation import compute_impacts
from boaviztapi.compute.verbose import verbose_storage
from boaviztapi.dto.storage import StorageService, mapper_storage

storage_router = APIRouter(prefix="/v1/storage", tags=["storage"])


@storage_router.post("")
async def storage_as_a_service_impact_from_configuration(
    storage: StorageService = Body(...),
    verbose: bool = True,
    duration: Optional[float] = config.default_duration,
    criteria: List[str] = Query(config.default_criteria),
):
    try:
        model = mapper_storage(storage)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    if duration is None:
        duration = model.usage.hours_life_time.value

    impacts = compute_impacts(
        model=model, selected_criteria=criteria, duration=duration
    )

    result: dict = {"impacts": impacts}
    if verbose:
        result["verbose"] = verbose_storage(
            model, selected_criteria=criteria, duration=duration
        )
    return result
