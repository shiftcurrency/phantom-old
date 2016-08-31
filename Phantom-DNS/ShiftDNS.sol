/// @title Phantom DNS contract.

contract ShiftDNS {

    struct RR {
        string addr;
        address owner;
        bool exist;
    }   

    struct SiteIndex {
        string domain;
        string siteAddr;
        bool exist;
    }

    mapping( string => RR ) rrs;
    mapping( string => SiteIndex ) index;
    address address1 = 0x82b5f6de85e6d5982992ee467808682b01a95e24;
    address address2 = 0x1050e68083a5378a02deec6a23368a788d23fd6c;
    address address3 = 0x1c581f7803508f4bc01e9b7595b220be2a5f1818;
    address address4 = 0xcad21b2e2c06d79d86411d1577714937c9c7aad9; 
    uint accountBalanceLimit;

    function setIndexingBalanceLimit(uint balance) returns (uint){
        if (msg.sender == address1 || msg.sender == address2 || msg.sender == address3 || msg.sender == address4) {
            accountBalanceLimit = balance;
            // Returns 0 if the update of balance check is successfully set.
            return 0;
        }
        // Returns 0 if the update of balance check fail.
        return 1;
    }

    function getBalanceLimit() returns (uint) {
        return accountBalanceLimit;
    }

    function indexSite(string owner, string _domain, string _phantom_addr) returns (uint) {

        // OBSERVE: You need a registered domain to be able to add your site to the global mesh index.

        // The account that calls the contract.
        address sndr = msg.sender;
        // The balance of the account that calls the contract.
        uint balance = sndr.balance;

        // Checks the account balance limit before indexing a site.
        if(balance >= accountBalanceLimit) {
            if(index[owner].exist == false) {
                index[owner].exist = true;
                index[owner].domain = _domain;
                index[owner].siteAddr = _phantom_addr;
                // Returns 0 on success.
                return 0;
            }
            // Returns 1 if the domain is already registered.
            return 1;
        }
        // Returns 2 if there is unsufficient funds.
        return 2;
    }

    function searchIndex(string addr) returns (string) {
        if(index[addr].exist == true) {
            return index[addr].domain;
        }
        return "false";
    }

    function setRR(string _domain, string _address) returns (uint){
        // Check if the domain exists, else register it. 
        if(rrs[_domain].exist == false) {
            rrs[_domain].addr = _address;
            rrs[_domain].owner = msg.sender;
            rrs[_domain].exist = true;
            return 0;
        }   
        return 1;
    }   

    // Return the Phantom bitcoin hash address for the site.
    function getRR(string _domain) returns (string) {
        if(rrs[_domain].exist == true) {
            return rrs[_domain].addr;
        }
        return "false";
    }   
}
