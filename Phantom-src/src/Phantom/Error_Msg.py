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
        return  {"jsonrpc": "2.0", "id": "1", "result": ["false", "No method specified"]}
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
    else:
        return {"jsonrpc": "2.0", "id": "1", "result": ["false", "Unhandled exception. Please check the log file and report to Shift"]}
