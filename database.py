import sqlite3

class AnalyticsDatabase:
    events_table = 'events'

    @classmethod
    def clicks_connection(cls):
        return sqlite3.connect('clicks.sqlite3')

    @classmethod
    def setup(cls):
        cls.conn = cls.clicks_connection()
        cls.conn.execute(f'CREATE TABLE IF NOT EXISTS "{cls.events_table}" (id INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT, timestamp TIMESTAMP, user_agent TEXT, ip TEXT)')
        cls.conn.commit()

    @classmethod
    def track_click(cls, request):
        cls.conn = cls.clicks_connection()
        cls.conn.execute(f'INSERT INTO "{cls.events_table}" (event, timestamp, user_agent, ip) VALUES (?, datetime("now"), ?, ?)', (request.path, request.user_agent.string, request.remote_addr))
        cls.conn.commit()

    @classmethod
    def get_stats(cls) -> dict:
        cls.conn = cls.clicks_connection()
        print(cls.events_table)
        result = cls.conn.execute(f'SELECT event, COUNT(id) AS  FROM "{cls.events_table}" GROUP BY event')

