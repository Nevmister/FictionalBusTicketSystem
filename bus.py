class Bus:
    """Represents a physical bus assigned to a service and a bus model."""

    def __init__(self, id: int, service_id: int, bus_model_id: int, usage: str):
        self.id = id
        self.service_id = service_id
        self.bus_model_id = bus_model_id
        self.usage = usage

    def __repr__(self) -> str:
        return (
            f"Bus(id={self.id}, service_id={self.service_id}, "
            f"bus_model_id={self.bus_model_id}, usage='{self.usage}')"
        )