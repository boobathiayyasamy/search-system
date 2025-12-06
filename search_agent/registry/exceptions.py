"""Custom exceptions for the agents registry module."""


class RegistryError(Exception):
    """Base exception for all registry-related errors."""
    pass


class ConfigurationError(RegistryError):
    """Raised when there's an error parsing or validating the YAML configuration."""
    pass


class AgentLoadError(RegistryError):
    """Raised when an agent fails to load from its module."""
    pass


class AgentNotFoundError(RegistryError):
    """Raised when an agent module or instance cannot be found."""
    pass


class ToolLoadError(RegistryError):
    """Raised when a tool fails to load from its module."""
    pass
