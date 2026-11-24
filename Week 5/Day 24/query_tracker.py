"""
Day 24 SQL Query Tracker
Hooks into SQLAlchemy engine execution events to precisely count SQL statements emitted during GraphQL resolution.
Used for investigating and proving N+1 query patterns.
"""

from contextlib import contextmanager
from sqlalchemy import event


class QueryTracker:
    """Tracks queries executed on the SQLAlchemy engine within a monitored context."""
    def __init__(self, engine):
        self.engine = engine
        self.queries = []
        self._listener_fn = self._record_query

    def _record_query(self, conn, cursor, statement, parameters, context, executemany):
        # Ignore transaction boundary markers (BEGIN, COMMIT, ROLLBACK)
        stmt_upper = statement.strip().upper()
        if not stmt_upper.startswith(("BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT")):
            self.queries.append(statement)

    @contextmanager
    def capture(self):
        """Context manager capturing all queries executed during the block."""
        self.queries.clear()
        event.listen(self.engine, "before_cursor_execute", self._listener_fn)
        try:
            yield self
        finally:
            event.remove(self.engine, "before_cursor_execute", self._listener_fn)

    @property
    def count(self) -> int:
        return len(self.queries)
