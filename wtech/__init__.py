from .http import app
from .auto_check import get_web_text,get_web_for_json
from .dcBot import setup_bot, add_command

__all__ = ["app","get_web_text","get_web_for_json",'setup_bot', 'add_command']
