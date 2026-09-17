class BusModel:
    """Represents a bus model and its seating capacity."""

    def __init__(self, id: int, name: str, seats: int):
        self.id = id
        self.name = name
        self.seats = seats

    def __repr__(self) -> str:
        return f"BusModel(id={self.id}, name='{self.name}', seats={self.seats})"