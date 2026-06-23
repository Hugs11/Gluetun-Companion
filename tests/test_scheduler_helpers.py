import sqlite3
import unittest

from app.scheduler import _docker_start_event_matches_container, _mapping_get


class SchedulerHelperTest(unittest.TestCase):
    def test_mapping_get_supports_sqlite_row_without_get_method(self):
        conn = sqlite3.connect(':memory:')
        conn.row_factory = sqlite3.Row
        conn.execute('CREATE TABLE sample (name TEXT, enabled INTEGER)')
        conn.execute('INSERT INTO sample VALUES (?, ?)', ('FR#208', 1))
        row = conn.execute('SELECT * FROM sample').fetchone()

        self.assertEqual(_mapping_get(row, 'name'), 'FR#208')
        self.assertEqual(_mapping_get(row, 'missing', 'fallback'), 'fallback')

    def test_docker_event_filter_ignores_test_gluetun_container(self):
        event = {
            'Action': 'start',
            'Actor': {'Attributes': {'name': 'gluetun-companion-test'}},
        }

        self.assertFalse(_docker_start_event_matches_container(event, 'gluetun'))

    def test_docker_event_filter_accepts_target_container(self):
        event = {
            'Action': 'start',
            'Actor': {'Attributes': {'name': 'gluetun'}},
        }

        self.assertTrue(_docker_start_event_matches_container(event, 'gluetun'))


if __name__ == '__main__':
    unittest.main()
