def error_response(error_type):

    if error_type == "ipc_call_error":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "IPC call error"]}
    elif error_type == "invalid_domain":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Invalid domain"]}
    elif error_type == "invalid_wallet_addr":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Invalid wallet address"]}
    elif error_type == "invalid_amount":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Invalid amount"]}
    elif error_type == "empty_password":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Empty password string"]}
    elif error_type == "invalid_json_req":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Invalid JSON request"]}
    elif error_type == "invalid_json_ver":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Invalid version of JSON-RPC specification"]}
    elif error_type == "missing_params":
        return  {"jsonrpc": "2.0", "id": "1", "result": ["false", "Missing parameters in JSON array"]}
    elif error_type == "no_method":
        return  {"jsonrpc": "2.0", "id": "1", "result": ["false", "Method not recognized or specified"]}
    elif error_type == "err_create_sitedir":
        return  {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not create site directory"]}
    elif error_type == "err_create_site":
        return  {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not create site"]}
    elif error_type == "err_sign_site":
        return  {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not sign site"]}
    elif error_type == "invalid_parameters":
        return  {"jsonrpc": "2.0", "id": "1", "result": ["false", "Invalid parameter(s)"]}
    elif error_type == "invalid_hex_string":
        return  {"jsonrpc": "2.0", "id": "1", "result": ["false", "Not a valid hex string as parameter"]}
    elif error_type == "no_params_allowed":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "No parameters allowed for this method"]}
    elif error_type == "sign_missing_params":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Site address and private key is needed for publishing a new site"]}
    elif error_type == "err_gen_ident":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not generate new identity for messaging"]}
    elif error_type == "err_create_filter":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not create filter"]}
    elif error_type == "err_store_data":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not store data in phantom database"]}
    elif error_type == "err_select_data":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not retrieve data from phantom database"]}
    elif error_type == "no_filters":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "No filter id's could be found in phantom database"]}
    elif error_type == "ipc_inv_handle":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Invalid IPC handle. Could not connect to Gshift"]}
    elif error_type == "ipc_err_open":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not open IPC named pipe"]}
    elif error_type == "ipc_setstate_err":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not set pipe handle state"]}
    elif error_type == "ipc_err_write":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not write to named pipe"]}
    elif error_type == "ipc_buff_overflow":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not retrieve more data from named pipe, buffer overflow"]}
    elif error_type == "err_trans_hist":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not retrieve any transaction history"]}
    elif error_type == "err_store_addrbook":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not store address and alias in address book"]}
    elif error_type == "err_addr_book":
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Could not retrieve address book"]}
    else:
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Unhandled exception. Please check the log file and report to Shift"]}
