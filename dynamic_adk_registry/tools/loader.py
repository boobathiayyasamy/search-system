import importlib
import logging
from typing import Any, Callable

from ..exceptions import ToolLoadError

logger = logging.getLogger(__name__)


class ToolLoader:
    
    def load_tool_from_module(self, module_path: str, function_name: str) -> Any:
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ToolLoadError(f"Failed to import module '{module_path}': {e}")
        
        if not hasattr(module, function_name):
            raise ToolLoadError(f"Function '{function_name}' not found in module '{module_path}'")
        
        tool_function = getattr(module, function_name)
        
        if not callable(tool_function):
            raise ToolLoadError(f"'{function_name}' in module '{module_path}' is not callable")
        
        try:
            tool = tool_function()
            logger.info(f"Loaded tool '{function_name}' from module '{module_path}'")
            return tool
        except Exception as e:
            raise ToolLoadError(f"Failed to execute '{function_name}' from '{module_path}': {e}")
