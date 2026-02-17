from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class PlayerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class PlayerResponse(BaseModel):
    id: int
    name: str
    total_wins: int = 0
    total_losses: int = 0
    matches_played: int = 0
    favorite_character: Optional[str] = None
    created_at: str


class ScoreCreate(BaseModel):
    player_id: int
    score: int
    character_used: str
    difficulty: str = "normal"


class ScoreResponse(BaseModel):
    id: int
    player_id: int
    score: int
    character_used: str
    difficulty: str
    created_at: str


class LeaderboardEntry(BaseModel):
    id: int
    player_id: int
    player_name: str
    score: int
    character_used: str
    difficulty: str
    created_at: str


class SessionCreate(BaseModel):
    player_id: int
    character_selected: str
    difficulty: str = "normal"


class SessionUpdate(BaseModel):
    result: Optional[str] = None
    score: Optional[int] = None
    ended_at: Optional[str] = None


class SessionResponse(BaseModel):
    id: int
    player_id: int
    character_selected: str
    difficulty: str
    result: Optional[str] = None
    score: int = 0
    started_at: str
    ended_at: Optional[str] = None


class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None