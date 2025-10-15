import enum

class TokenScope(str, enum.Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"