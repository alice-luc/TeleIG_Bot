import itertools

from utils.db_api.sqlite import Database

data_base = Database()


def test():
    # data_base.delete_ig_table()
    # data_base.create_users_ig()
    # data_base.trial_add_user('23534', '0r0')
    # data_base.ig_add_user('2357034', 'alohayog', '0r0')
    # data_base.update_membership('0riv0')
    # login = input()
    # tg_id = input()
    # membership = data_base.check_membership(tg_id, login)

    user = data_base.ig_select_user(24285, 'ser')
    print(user)


test()
