from typing import List, Optional
from datetime import datetime, timezone


class UserModel:
    def __init__(self, identifier: str, secret: str, hashed_codes: List[str],created_at: Optional[datetime] = None):
        self.identifier = identifier
        self.secret = secret
        self.hashed_codes = hashed_codes
        self.created_at = created_at or datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "identifier": self.identifier,
            "secret": self.secret,
            "hashed_codes": self.hashed_codes,
            "created_at": self.created_at,
        }
