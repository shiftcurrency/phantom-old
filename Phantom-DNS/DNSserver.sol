/*
Shift DNS server
*/
contract DNSserver {
	address creator;

	mapping (address => uint8) operators;
	mapping (string => string) DNSs;

    //initialization
    function DNSserver() {
        creator  =  msg.sender;
		operators[creator] = 1; //1 can add DNS, normal can not do it
    }   

    function addOperator(address _addr) {
		operators[_addr] = 1;
	}

	modifier onlyOperator()
    {
		if (operators[msg.sender] != 1) throw;
		_							
    }

	function addDNS(string _domain, string _walletString)
		onlyOperator 
	{
		DNSs[_domain] = _walletString;
	}

	function searchDNS(string _domain) returns(string) {
		string memory s1 = '';
		s1 = DNSs[_domain];
		return(s1);
	}

	// kills this contract
	function kill() { 
        if (msg.sender == creator)
            suicide(creator); 
    }	
}
