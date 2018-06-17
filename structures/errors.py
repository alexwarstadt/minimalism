class InteractionError(Exception):
    """
    Raise whenever a user's input is uninterpretable or violates requirements from definitions
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "\nALERT: %s\n" % self.message