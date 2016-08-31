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
    uint accountBalance;

    function siteIndexBalance(uint balance) returns (uint){
        if (msg.sender == address1) {
            accountBalance = balance;
            // Returns 0 if the update of balance check is successfully set.
            return 0;
        }
        // Returns 0 if the update of balance check fail.
        return 1;
    }
            

    function setRR(string _domain, string _address) returns (bool){
        // Check if the domain exists, else register it. 
        if(rrs[_domain].exist == false) {
            rrs[_domain].addr = _address;
            rrs[_domain].owner = msg.sender;
            rrs[_domain].exist = true;
            return true;
        }
        return false;
    }

    function indexSite(string owner, string _domain, string _phantom_addr) returns (uint) {

        // The account that calls the contract.
        address sndr = msg.sender;
        // The balance of the account that calls the contract.
        uint balance = sndr.balance;

        // Checks the account balance limit before creating a domain.
        if(balance >= accountBalance) {
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
        // Balance check is already done since phantom use the function indexSite to resolve domain names.
        // You can index a site, but it wont get indexed if a registered domain does not exist.
        if(index[addr].exist == true) {
            return index[addr].domain;
        }
        return "false";
    }

    // Return the Phantom bitcoin hash address for the site.
    function getRR(string _domain) returns (string) {
        return rrs[_domain].addr;
    }   
}
