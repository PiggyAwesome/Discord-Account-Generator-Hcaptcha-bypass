class HCaptchaError(Exception):
    pass

class SolveFailure(HCaptchaError):
    pass

class APITimeout(HCaptchaError):
    pass

class HCaptchaFailure(HCaptchaError):
    pass