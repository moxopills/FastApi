from fastapi import APIRouter

from app.dtos.create_participant_request import CreateParticipantRequest
from app.dtos.create_participant_response import CreateParticipantMysqlResponse

mysql_router = APIRouter(
    prefix="/v1/mysql/participants",
    tags=["participants"],
)


@mysql_router.post("", description="participants create")
async def api_create_participant_mysql(
    create_participant_request: CreateParticipantRequest,
) -> CreateParticipantMysqlResponse:
    return CreateParticipantMysqlResponse(participant_id=123, participant_dates=[])
