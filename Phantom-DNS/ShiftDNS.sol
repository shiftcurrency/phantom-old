contract ShiftDNS{
    
    struct RR {
        string addr;
        address owner;
        bool exist;
    }
    
    mapping( string => RR ) rrs;

    uint256[] domains;

    function addDomainList(uint256 domain) {
        domains.push(domain);
    }

    function getDomainList() returns (uint256[]) {
        return domains;
    }
    
    function setRR(string _domain, string _address) returns (bool){
        if(rrs[_domain].exist == false) {
            rrs[_domain].addr = _address;
            rrs[_domain].owner = msg.sender;
            rrs[_domain].exist = true;
            return true;
        }
        return false;
    }

    function getRR(string _domain) returns (string) {
        return rrs[_domain].addr;
    }
}
