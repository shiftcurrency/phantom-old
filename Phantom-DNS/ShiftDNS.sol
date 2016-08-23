/// @title Phantom DNS contract.

contract ShiftDNS {

    uint256[] domains;

    struct RR {
        string addr;
        address owner;
        bool exist;
    }   
 
    mapping( string => RR ) rrs;
    address creator = msg.sender;

    // On registration of a Phantom domain we index the domain
    // in an array to be searchable by Phantom network.
    function addDomainList(uint256 domain) returns(uint) {
        domains.push(domain);
    }

    function getDomainList() returns (uint256[]) {
        return domains;
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

    function getRR(string _domain) returns (string) {
        return rrs[_domain].addr;
    }   

    // kills this contract
    function kill() { 
        if (msg.sender == creator)
            suicide(creator);
    }
}
