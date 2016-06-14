import sqlite3
import Error_Msg

class PhantomDb(object):

    conn = sqlite3.connect('src/Phantom/phantom.db')
    c = conn.cursor()

    def init_database(self):
        try:
            self.c.execute('CREATE TABLE IF NOT EXISTS messaging (identity TEXT, filter_id INTEGER)')
            self.conn.commit()
            self.c.execute('CREATE TABLE IF NOT EXISTS trans_history (date TEXT, from_account TEXT, to_account TEXT, amount TEXT)')
            self.conn.commit()
            self.c.execute('CREATE TABLE IF NOT EXISTS address_book (toaddress TEXT, alias TEXT)')
            self.conn.commit()
        except Exception as e:
            return False
        return True


    def clear_database(self):
        try:
            self.c.execute('DELETE FROM messaging')
            self.conn.commit()
        except Exception as e:
            return False
        return True


    def store_filter(self, store_dict):
        if len(store_dict) > 0 and 'to' in store_dict and 'filter_id' in store_dict and \
            store_dict['filter_id'] != "" and store_dict['to'] != "":
                try:
                    sql = "INSERT OR IGNORE INTO messaging (identity, filter_id) VALUES (\"%s\",%i)" % (store_dict['to'], store_dict['filter_id'])
                    self.c.execute(sql)
                    self.conn.commit()
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
            self.conn.commit()
        except Exception as e:
            return False
        return True

    def store_address_book(self, to_account, alias):

        try:
            sql = "INSERT OR IGNORE INTO address_book (toaddress, alias) VALUES (\"%s\", \"%s\")" % (to_account, alias)
            self.c.execute(sql)
            self.conn.commit()
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


    def get_transaction_hist(self):
        
        try:
            self.c.execute('SELECT * FROM trans_history')
            res = self.c.fetchall()
        except Exception as e:
            return False
        return res
