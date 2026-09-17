class Run:
    """Represents an instance of a service on a particular day."""

    def __init__(self, id: int, service_id: int, run_date: str):
        self.id = id
        self.service_id = service_id
        self.run_date = run_date

    def __repr__(self) -> str:
        return (
            f"Run(id={self.id}, service_id={self.service_id}, "
            f"run_date='{self.run_date}')"
        )