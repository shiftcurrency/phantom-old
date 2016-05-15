import sqlite3
import Error_Msg

class PhantomDb(object):

    conn = sqlite3.connect('src/Phantom/phantom.db')
    c = conn.cursor()

    def init_database(self):
        try:
            self.c.execute('CREATE TABLE IF NOT EXISTS messaging (identity TEXT, filter_id INTEGER)')
            self.conn.commit()
        except Exception as e:
            return Error_Msg.error_response("err_store_data")

        return True


    def clear_database(self):
        try:
            self.c.execute('DELETE FROM messaging')
            self.conn.commit()
        except Exception as e:
            return Error_Msg.error_response("err_store_data")
        
        return True


    def store_data(self, store_dict):
        if len(store_dict) > 0 and 'to' in store_dict and 'filter_id' in store_dict and \
            store_dict['filter_id'] != "" and store_dict['to'] != "":
                try:
                    sql = "INSERT OR IGNORE INTO messaging (identity, filter_id) VALUES (\"%s\",%i)" % (store_dict['to'], store_dict['filter_id'])
                    self.c.execute(sql)
                    self.conn.commit()
                except Exception as e:
                    return Error_Msg.error_response("err_store_data")
                
                return True
        return Error_Msg.error_response("err_store_data")
