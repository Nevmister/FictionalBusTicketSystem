class Service:
    """Represents a bus service from one place to another at a given time."""

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f"Service(id={self.id}, name='{self.name}')"