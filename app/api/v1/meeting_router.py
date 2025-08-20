from fastapi import APIRouter

from app.dtos.create_meeting_response import CreateMeetingResponse

edgedb_router = APIRouter(prefix="/v1/edgedb/meeting", tags=["Meeting"],redirect_slashes=False)
mysql_router = APIRouter(prefix="/v1/mysql/meeting", tags=["Meeting"],redirect_slashes=False)
#원래는 어떤 DB를 쓰는지 url에 적을 필요없음
#실전에선 DB이름 url에 넣지 말기

@edgedb_router.post(
    "",
    description="meeting 을 생성합니다.",
)
async  def api_create_meeting_edgedb() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code="abc")

@mysql_router.post(
    "",
    description="meeting 을 생성합니다."
)
async def api_create_meeting_mysql() -> CreateMeetingResponse:
    return CreateMeetingResponse(url_code="abc")