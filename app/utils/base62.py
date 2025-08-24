import string
from typing import Final


class Base62:
    # 더 일반적인 순서: 숫자 -> 소문자 -> 대문자
    BASE: Final[str] = string.digits + string.ascii_lowercase + string.ascii_uppercase
    BASE_LEN: Final[int] = len(BASE)

    @classmethod
    def encode(cls, num: int) -> str:
        if num < 0:
            raise ValueError(f"{cls}.encode() needs positive integer but you passed: {num}")

        if num == 0:
            return cls.BASE[0]

        result = []
        while num:
            num, remainder = divmod(num, cls.BASE_LEN)
            result.append(cls.BASE[remainder])
        return "".join(reversed(result))
