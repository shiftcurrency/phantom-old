contract ShiftDNS{
    
    struct RR {
        string addr;
        address owner;
        bool exist;
    }
    
    mapping( string => RR ) rrs;
    
    function setRR(string _domain, string _address){
        if(rrs[_domain].exist == false) {
            rrs[_domain].addr = _address;
            rrs[_domain].owner = msg.sender;
            rrs[_domain].exist = true;
        }
    }

    function getRR(string _domain) returns (string) {
        return rrs[_domain].addr;
    }
}
