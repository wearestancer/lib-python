from stancer.exceptions import StancerNotImplementedError


class DeleteSetterError(StancerNotImplementedError):
    """Raised when we try to set a deleted from the sdk"""
