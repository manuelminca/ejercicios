from shutil import ExecError
import sqlite3

def init_db(cur):
    cur.execute("""
        create table savings(
            userid text primary key,
            amount integer not null
        )
    """)

def create_user(cur, userid, amount):
    cur.execute("insert into savings(userid, amount) values (?, ?)", (userid, amount))

def get_credit(cur, userid):
    cur.execute("select amount from savings where userid = ?", (userid,))
    return cur.fetchone()[0]

def set_credit(cur, userid, amount):
    cur.execute("update savings set amount = ? where userid = ?", (amount, userid))
    
def set_credit_fail(cur, userid, amount):
    print("in setcredit 2")
    cur.execute("update savings set amount = ? where ssfg = ?", (amount, userid))

def transfer(cur, user_a, user_b, transfer_amount, fail=False):

    user_a_credit = get_credit(cur, user_a)
    assert user_a_credit >= transfer_amount

    user_b_credit = get_credit(cur, user_b)

    new_user_a_credit = user_a_credit - transfer_amount
    set_credit(cur, user_a, new_user_a_credit)
    new_user_b_credit = user_b_credit + transfer_amount

    if fail: 
        set_credit_fail(cur, user_b, new_user_b_credit)
        print("no deberia entrar")
    else:
        set_credit(cur, user_b, new_user_b_credit)


