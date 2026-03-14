"""Conversation context utility for weekly scripts."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ContextManager:
    """Store and resolve short multi-turn context."""

    max_turns: int = 3
    last_intent: Optional[str] = None
    last_entities: Dict[str, List[str]] = field(
        default_factory=lambda: {"dates": [], "course_codes": [], "semester": []}
    )
    history: List[Dict[str, str]] = field(default_factory=list)

    def resolve(self, intent: Optional[str], entities: Dict[str, List[str]]) -> Tuple[str, Dict[str, List[str]]]:
        """Resolve missing intent/entities from previous turn."""
        resolved_intent = intent or self.last_intent or "unknown"
        resolved_entities = dict(entities)
        for key in ("dates", "course_codes", "semester"):
            if not resolved_entities.get(key) and self.last_entities.get(key):
                resolved_entities[key] = self.last_entities[key]
        return resolved_intent, resolved_entities

    def update(self, user: str, bot: str, intent: str, entities: Dict[str, List[str]]):
        """Update context and keep only latest turns."""
        self.last_intent = intent
        self.last_entities = entities
        self.history.append({"user": user, "bot": bot})
        self.history = self.history[-self.max_turns :]
