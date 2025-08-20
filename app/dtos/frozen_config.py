from pydantic import ConfigDict

FROZEN_CONFIG = ConfigDict(frozen=True)
# frozen -> 얼어있는 상태
# 얼어있는 객체는 -> 생성 이후에는 변경할 수 없는 객체
# immutable
