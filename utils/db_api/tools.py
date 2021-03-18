import itertools

from utils.db_api.sqlite import Database

db = Database()


def test():
    # db.delete_ig_table()
    # db.create_users_ig()
    # db.trial_add_user('23534', '0r0')
    # db.ig_add_user('2357034', 'alohayog', '0r0')
    # db.update_membership('0riv0')
    # login = input()
    # tg_id = input()
    # membership = db.check_membership(tg_id, login)

    user = db.ig_select_user(24285, 'ser')
    print(user)


test()
