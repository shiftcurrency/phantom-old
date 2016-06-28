import sqlite3
import Error_Msg
from Shift_IPC import IPC_Client
from time import sleep

class PhantomDb(object):

    conn_phantom = sqlite3.connect('src/Phantom/phantom.db')
    c = conn_phantom.cursor()

    client = IPC_Client.Client()
    shiftdb = client.get_shiftdb_path()

    for i in range(2):
        try:
            conn_shiftdb = sqlite3.connect(shiftdb)
            x = conn_shiftdb.cursor()
        except Exception as e:
            print "Waiting for shift.db..."
            sleep(5)
        

    def init_database(self):
        try:
            self.c.execute('CREATE TABLE IF NOT EXISTS messaging (identity TEXT, filter_id INTEGER)')
            self.conn_phantom.commit()
            self.c.execute('CREATE TABLE IF NOT EXISTS address_book (toaddress TEXT PRIMARY KEY NOT NULL, alias TEXT)')
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

    def del_address_book(self, to_account):
        
        try:
            sql = "DELETE FROM address_book WHERE toaddress = \"%s\"" % (to_account)
            self.c.execute(sql)
            self.conn_phantom.commit()
        except Exception as e:
            return False
        return True
        
    def store_address_book(self, to_account, alias):

        try:
            sql = "INSERT OR REPLACE INTO address_book (toaddress, alias) VALUES (\"%s\", \"%s\")" % (to_account, alias)
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


    def get_balance_by_block(self, account, blocknum):

        try:
            sql_sent_amount = "SELECT datetime,max(blocknumber),hash,sum(amount) FROM txs WHERE sender = \"%s\" AND blocknumber <= %i" % (account, blocknum)
            sql_rec_amount = "SELECT datetime,max(blocknumber),hash,sum(amount) FROM txs WHERE recipient = \"%s\" AND blocknumber <= %i" % (account, blocknum)
            self.x.execute(sql_sent_amount)
            sent = self.x.fetchall()
            self.x.execute(sql_rec_amount)
            rec = self.x.fetchall()

        except Exception as e:
            return False

        if len(sent) == 1 and len(sent[0]) == 4:
            if len(rec) == 1 and len(rec[0]) == 4:
                return [ str(sent[0][0]), str(sent[0][1]), str(sent[0][2]), str(float(sent[0][3])/1000000000000000000) ]
        return False
