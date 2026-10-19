"""Count the statements an engine sends to the database, for part B."""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from sqlalchemy import Engine, event


@dataclass
class StatementCount:
    statements: int = 0


@contextmanager
def count_statements(engine: Engine) -> Iterator[StatementCount]:
    """Count every statement sent through `engine` inside the `with` block.

    with count_statements(engine) as counted:
        ...
    counted.statements    # also printed when the block ends
    """
    counted = StatementCount()

    # Called once for each statement, just before it goes to the database.
    # BEGIN and ROLLBACK in the log are not statements the ORM wrote, and are not
    # counted.
    def count(*_: object) -> None:
        counted.statements += 1

    event.listen(engine, "before_cursor_execute", count)
    try:
        yield counted
    finally:
        event.remove(engine, "before_cursor_execute", count)
        print(f"statements sent: {counted.statements}")
