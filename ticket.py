class Ticket:
    """Represents a ticket owned by a user for a specific run."""

    def __init__(self, id: int, user_id: int, run_id: int):
        self.id = id
        self.user_id = user_id
        self.run_id = run_id

    def __repr__(self) -> str:
        return (
            f"Ticket(id={self.id}, user_id={self.user_id}, run_id={self.run_id})"
        )