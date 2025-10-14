from enum import Enum as PyEnum
class InvitationStatus(PyEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"