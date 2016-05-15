import sqlite3
import Error_Msg

class PhantomDb(object):

    def __init__(self, store_dict)
        if len(store_dict) == 0:
            return Error_Msg.error_response("err_store_data")

        try:
            conn = sqlite3.connect('phantom.db')
            c = conn.cursor()
        except Exception as e:
            return Error_Msg.error_response("err_store_data")


    def init_database(self):
        try:
            c.execute('CREATE TABLE IF NOT EXIST messaging (identity TEXT, filter_id INTEGER)')
            conn.commit()
        except Exception as e:
            return Error_Msg.error_response("err_store_data")

        return True


    def clear_database(self):
        try:
            c.execute('DELETE FROM messaging')
            conn.commit()
        except Exception as e:
            return Error_Msg.error_response("err_store_data")
        
        return True


    def store_data(self, store_dict):
        if 'to' in store_dict and 'filter_id' in store_dict and \
            store_dict['filter_id'] != "" and store_dict['to'] != "":
                try:
                    c.execute("INSERT OR IGNORE INTO messaging (identity, filter_id) VALUES (?,?)", store_dict['filter_id'], store_dict['to'],)
                    conn.commit()
                except Exception as e:
                    return Error_Msg.error_response("err_store_data")
                
                return True
        return Error_Msg.error_response("err_store_data")
