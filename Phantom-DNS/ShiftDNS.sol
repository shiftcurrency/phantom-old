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

        address sndr = msg.sender;
        uint balance = sndr.balance;

        if(balance >= 4000000000000000000000) {
            if(index[owner].exist == false) {
                index[owner].exist = true;
                index[owner].domain = _domain;
                index[owner].siteAddr = _phantom_addr;
                return 0;
            }
            return 1;
        }
        return 2;
    }

    function searchIndex(string addr) returns (string) {
        if(index[addr].exist == true) {
            return index[addr].domain;
        }
        return "false";
    }

    function getRR(string _domain) returns (string) {
        return rrs[_domain].addr;
    }   
}
