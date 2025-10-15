import enum

class Provider(str, enum.Enum):
    GOOGLE = "google"
    SPOTIFY = "spotify"

class Access(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class AuthorizationStatus(str, enum.Enum):
    ACTIVE = "active"           
    EXPIRED = "expired"         
    REVOKED = "revoked"         
    MISSING = "missing"         

class RegistrationStatus(str, enum.Enum):
    SIGNED_IN = "signed_in"                
    INVITATION_SENT = "invitation_sent"   
    INVITATION_ACCEPTED = "invitation_accepted"   
    NAMED_PET = "named_pet"               
    SPOTIFY_LINKED = "spotify_linked"     
    PERSONALITY_GENERATED = "personality_generated"  
    COMPLETE = "complete"