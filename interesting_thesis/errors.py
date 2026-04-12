class InterestingThesisError(Exception):
    """Base exception for the project."""


class ConfigurationError(InterestingThesisError):
    """Raised when the runtime configuration is invalid."""


class DocumentReadError(InterestingThesisError):
    """Raised when a document cannot be read."""


class MissingDependencyError(InterestingThesisError):
    """Raised when an optional runtime dependency is missing."""


class ModelResponseError(InterestingThesisError):
    """Raised when the model returns an unusable response."""
