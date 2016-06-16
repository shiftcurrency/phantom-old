import sqlite3
import Error_Msg
from Shift_IPC import IPC_Client

class PhantomDb(object):

    conn_phantom = sqlite3.connect('src/Phantom/phantom.db')
    c = conn_phantom.cursor()

    client = IPC_Client.Client()
    shiftdb = client.get_shiftdb_path()
    print shiftdb
    conn_shiftdb = sqlite3.connect(shiftdb)
    x = conn_shiftdb.cursor()

    def init_database(self):
        try:
            self.c.execute('CREATE TABLE IF NOT EXISTS messaging (identity TEXT, filter_id INTEGER)')
            self.conn_phantom.commit()
            self.c.execute('CREATE TABLE IF NOT EXISTS trans_history (date TEXT, from_account TEXT, to_account TEXT, amount TEXT)')
            self.conn_phantom.commit()
            self.c.execute('CREATE TABLE IF NOT EXISTS address_book (toaddress TEXT, alias TEXT)')
            self.conn_phantom.commit()
        except Exception as e:
            return False
        return True


    def clear_database(self):
        try:
            self.c.execute('DELETE FROM messaging')
            self.conn_phantom.commit()
        except Exception as e:
            return False
        return True


    def store_filter(self, store_dict):
        if len(store_dict) > 0 and 'to' in store_dict and 'filter_id' in store_dict and \
            store_dict['filter_id'] != "" and store_dict['to'] != "":
                try:
                    sql = "INSERT OR IGNORE INTO messaging (identity, filter_id) VALUES (\"%s\",%i)" % (store_dict['to'], store_dict['filter_id'])
                    self.c.execute(sql)
                    self.conn_phantom.commit()
                except Exception as e:
                    return False
                return True
        return False

    
    def get_latest_filter(self):

        try:
            self.c.execute('SELECT filter_id FROM messaging ORDER BY filter_id DESC LIMIT 1')
            res = self.c.fetchall()
        except Exception as e:
            return False

        return res


    def store_transaction_hist(self, from_account, to_account, amount):
        
        try:
            self.c.execute('SELECT CURRENT_TIMESTAMP')
            date = self.c.fetchall()
        except Exception as e:
            return False
        try:
            sql = "INSERT OR IGNORE INTO trans_history (date, from_account, to_account, amount) VALUES (\"%s\", \"%s\", \"%s\", \"%s\")" % (date[0][0], from_account, to_account, amount)
            self.c.execute(sql)
            self.conn_phantom.commit()
        except Exception as e:
            return False
        return True

    def store_address_book(self, to_account, alias):

        try:
            sql = "INSERT OR IGNORE INTO address_book (toaddress, alias) VALUES (\"%s\", \"%s\")" % (to_account, alias)
            self.c.execute(sql)
            self.conn_phantom.commit()
        except Exception as e:
            return False
        return True

    def get_address_book(self):
        
        try:
            self.c.execute('SELECT * FROM address_book')
            res = self.c.fetchall()
        except Exception as e:
            return False
        return res


    def get_transaction_hist(self, account):
        
        try:
            sql = "SELECT * FROM txs WHERE sender = \"%s\" OR recipient = \"%s\"" % (account, account)
            self.x.execute(sql)
            res = self.x.fetchall()
        except Exception as e:
            return False
        return res
