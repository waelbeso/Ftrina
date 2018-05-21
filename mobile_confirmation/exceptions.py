"Simple Mobile Confirmation Exceptions"


class SimpleMobileConfirmationException(Exception):
    pass


class MobileNotConfirmed(SimpleMobileConfirmationException):
    pass


class MobileConfirmationExpired(SimpleMobileConfirmationException):
    pass


class MobileIsPrimary(SimpleMobileConfirmationException):
    pass
