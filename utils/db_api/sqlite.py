"""
manipulations with database sqlite
"""
import itertools
import sqlite3
import datetime


class Database:
    """
    ig users database
    """
    def __init__(self, path_to_db='./volume_data/tg.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        """
        makes a connection to db
        """
        return sqlite3.connect(self.path_to_db)

    def delete_ig_table(self):
        """
        deletes insta table
        :return:
        """
        sql = 'DROP TABLE Users_IG'
        self.execute(sql, commit=True)

    def execute(self, sql: str, parameters: tuple = None,
                fetchone=False, fetchall=False, commit=False):
        """
        executes sql code containing in the sql variable
        """
        if not parameters:
            parameters = tuple()

        connection = self.connection
        # connection.set_trace_callback(logger)

        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None
        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()

        return data

    def create_users_ig(self):
        """
        creates a table if it does not exists yet
        """
        sql = '''
        CREATE TABLE Users_IG (
        id integer NOT NULL,
        tg_id VARCHAR NOT NULL,
        tg_username VARCHAR(255) NOT NULL,
        login VARCHAR(255) NOT NULL,
        status integer,
        purchase_ending DATE,
        proxy VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
        );'''
        self.execute(sql, commit=True)

    def create_trial_ig(self):
        """
        creates a table for trial subscription if it does not exists yet
        """
        sql = '''
        CREATE TABLE Trial_IG (
        id integer NOT NULL,
        tg_id integer NOT NULL,
        login VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
        );'''
        self.execute(sql, commit=True)

    def ig_add_user(self, tg_id: str, tg_username: str, login: str):
        """
        adds user into database
        """
        # from IgSide.dataIns import proxies_data
        sql = 'INSERT INTO Users_IG(tg_id, tg_username, login, status, purchase_ending, proxy) VALUES(?, ?, ?, ?, ?, ?)'
        # proxy = proxies_data[random.randrange(len(proxies_data))]
        parameters = (tg_id, tg_username, login, 0, 0, '104.227.99.250:8000')
        if not self.ig_select_user(tg_id, login):
            self.execute(sql, parameters=parameters, commit=True)
        else:
            return 'Вы уже регистрировали этот аккаунт'

    def ig_select_user(self, tg_id, login):
        """
        checks whether the user exists and returns one's data
        """
        sql = 'SELECT * FROM Users_IG WHERE tg_id = ? AND login = ?'
        user_row = self.execute(sql, parameters=(tg_id, login), fetchall=True)
        if user_row:
            user = list(itertools.chain.from_iterable(user_row))
            return user
        else:
            return None

    def update_membership(self, login):
        """
        makes subscription value to be equal 1 to be returned as true on subscription check
        """
        days = datetime.date.today()
        delta = datetime.timedelta(days=30)
        sql = 'UPDATE Users_IG SET status= ?, purchase_ending = ? WHERE login = ?'

        self.execute(sql, parameters=(1, days+delta, login), commit=True)

    def check_accounts(self, tg_id, tg_username):
        """
        returns a list of accounts(login + purchased date) that belong to this tg user. Returns None if there isnt any
        """
        sql = 'SELECT login, purchase_ending FROM Users_IG WHERE tg_id = ? AND tg_username = ?'
        users_row = self.execute(sql, parameters=(tg_id, tg_username), fetchall=True)
        if users_row:
            users = list(itertools.chain.from_iterable(users_row))
            return users
        else:
            return None

    def check_membership(self, tg_id, login):
        """
        returns True or False regarding to the proceed payment
        """
        tg_id = str(tg_id)
        sql = 'SELECT status FROM Users_IG WHERE tg_id = ? AND login = ?'
        status_row = self.execute(sql, parameters=(tg_id, login), fetchone=True)
        if status_row:
            status = status_row[0]  # needs to be tested, some requests were returning invalid data
            return status
        else:
            return None

    def minus_membership(self, login):
        """
        makes the value of status to be equal 0
        """
        sql = 'UPDATE Users_IG SET status= ? WHERE login = ?'
        self.execute(sql, parameters=(0, login), commit=True)

    def trial_select_user(self, tg_id, login):
        """
        checks whether the user has ran the trial version already and returns the one's data on success
        """
        tg_id = str(tg_id)
        sql = 'SELECT * FROM Trial_IG WHERE tg_id = ? AND login = ?'
        users_row = self.execute(sql, parameters=(tg_id, login), fetchall=True)
        if users_row:
            users = list(itertools.chain.from_iterable(users_row))
            return users
        else:
            return None

    def trial_add_user(self, tg_id: str, login: str):
        """
        adds user into trial_users database
        """
        sql = 'INSERT INTO Trial_IG(tg_id, login) VALUES(?, ?)'
        parameters = (tg_id, login)
        if not self.trial_select_user(tg_id, login):
            self.execute(sql, parameters=parameters, commit=True)
        else:
            return 'Вы уже регистрировали этот аккаунт'

    def global_check(self):
        """
        Suppose to check db every day on whether the subscription's still valid
        Could also add a notifying directly to the user to make him prolong the membership
        """
        days = datetime.date.today()
        sql = 'SELECT tg_id, login FROM Users_IG WHERE purchase_ending = ?'
        parameters = (days,)
        users_row = self.execute(sql, parameters=parameters, commit=True)
        if users_row:
            users = list(itertools.chain.from_iterable(users_row))
            for user in users:
                print(user)


# def logger(statement):
#     """
#     provides stdout logging to simply watch the process
#     """
#     print(f"""
#
#
#
#     Executing:
#     {statement}
#
#
#     """)
