class ErrOrganizationNotFound(Exception):
    def __init__(self, message="Organization not found"):
        self.message = message
        super().__init__(self.message)

class ErrOrganizationCreate(Exception):
    def __init__(self, message="Failed to create organization"):
        self.message = message
        super().__init__(self.message)

class ErrOrganizationUpdate(Exception):
    def __init__(self, message="Failed to update organization"):
        self.message = message
        super().__init__(self.message)

class ErrOrganizationDelete(Exception):
    def __init__(self, message="Failed to delete organization"):
        self.message = message
        super().__init__(self.message)

class ErrInsufficientBalance(Exception):
    def __init__(self, message="Insufficient balance"):
        self.message = message
        super().__init__(self.message)