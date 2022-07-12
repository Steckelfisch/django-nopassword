import logging
from rest_framework.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


class UserNotValid(PermissionDenied):
    def __init__(self, detail=None, code=None):
        super(UserNotValid, self).__init__(detail=detail, code=code)