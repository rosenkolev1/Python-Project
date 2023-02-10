
class InvalidMoneyForSettingsException(Exception):

    def __init__(self, message="The money is invalid for the given game settings!"):
        self.message = message
        super().__init__(self.message)