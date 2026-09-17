class User:
    """Represents a system user."""

    def __init__(self, id: int, admin: bool, username: str, password: str):
        self.id = id
        self.admin = admin
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, admin={self.admin}, "
            f"username='{self.username}', password='{self.password}')"
        )