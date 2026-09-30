"""Skills and action handlers package."""
from jarvis.skills.registry import SkillRegistry
from jarvis.skills.vlc_player import VLCController
from jarvis.skills.weather import WeatherSkill
from jarvis.skills.web_search import WebSkill

__all__ = ["SkillRegistry", "VLCController", "WeatherSkill", "WebSkill"]
