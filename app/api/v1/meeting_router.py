from fastapi import APIRouter

from app.dtos.create_meeting_response import CreateMeetingResponse
from app.dtos.get_meeting_response import GetMeetingResponse
from app.tortoise_models.meeting import MeetingModel

mysql_router = APIRouter(
    prefix="/v1/mysql/meetings",
    tags=["Meeting"],
    redirect_slashes=False,
)


@mysql_router.post(
    "",
    description="meeting 을 생성합니다.",
    response_model=CreateMeetingResponse,
)
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    meeting = await MeetingModel.create_meeting(url_code="abc")
    return CreateMeetingResponse(url_code=meeting.url_code)


@mysql_router.get(
    "/{meetings/_url_code}",
    description="meeting을 조회합니다.",
)
async def api_get_meeting_mysql(meeting_url_code: str) -> GetMeetingResponse:
    return GetMeetingResponse(url_code="minsoo")
