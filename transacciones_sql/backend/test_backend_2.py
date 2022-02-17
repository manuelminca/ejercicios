import unittest
import sqlite3
from contextlib import closing
from backend.savings_backend_2 import init_db, create_user, get_credit, set_credit, transfer

class Test(unittest.TestCase):

    def test_basic_ops(self):
        conn = sqlite3.connect(':memory:')

        with closing(conn.cursor()) as cur:
            init_db(cur)
            create_user(cur, 'pepe', 100)

            self.assertEqual(get_credit(cur, 'pepe'), 100)

    def test_successful_transfer(self):
        conn = sqlite3.connect(':memory:')

        try:
            with conn:
                with closing(conn.cursor()) as cur:
                    init_db(cur)

                    create_user(cur, 'pepe', 100)
                    create_user(cur, 'paco', 100)

                    transfer(cur, 'pepe', 'paco', 50)

                    self.assertEqual(get_credit(cur, 'pepe'), 50)
                    self.assertEqual(get_credit(cur, 'paco'), 150)
        except sqlite3.Error:
            print("Rollback!")

    def test_insufficient_funds_transfer(self):
        conn = sqlite3.connect(':memory:')

        try:
            with conn:
                with closing(conn.cursor()) as cur:
                    init_db(cur)

                    create_user(cur, 'pepe', 100)
                    create_user(cur, 'paco', 100)

                    with self.assertRaises(Exception):
                        transfer(cur, 'pepe', 'paco', 1000)
        except sqlite3.Error:
            print("Rollback!")

    def test_light_cut(self):
        conn = sqlite3.connect(':memory:')
        cur = conn.cursor()
        init_db(cur)
        create_user(cur, 'pepe', 100)
        create_user(cur, 'paco', 100)

        try:
            with cur:
                with self.assertRaises(Exception):
                    transfer(cur, 'pepe', 'paco', 50, True)
                raise Exception
        except:
            pass
        
        self.assertEqual(get_credit(cur, 'pepe'), 100)       
        self.assertEqual(get_credit(cur, 'paco'), 100)

    def test_quick(self):
        conn = sqlite3.connect(':memory:')
        cur = conn.cursor()
        init_db(cur)
        create_user(cur, 'pepe', 100)

        try:
            with cur:
                set_credit(cur, 'pepe', 500)

                raise Exception
        except:
            pass
        
        cur.execute("select * from savings")
        print(cur.fetchone())
        
