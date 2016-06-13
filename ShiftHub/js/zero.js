/* ---- ZeroFrame ---- */


(function() {
  var ZeroFrame,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __slice = [].slice;

  ZeroFrame = (function() {
    function ZeroFrame(url) {
      this.onCloseWebsocket = __bind(this.onCloseWebsocket, this);
      this.onOpenWebsocket = __bind(this.onOpenWebsocket, this);
      this.route = __bind(this.route, this);
      this.onMessage = __bind(this.onMessage, this);
      this.url = url;
      this.waiting_cb = {};
      this.connect();
      this.next_message_id = 1;
      this.init();
    }

    ZeroFrame.prototype.init = function() {
      return this;
    };

    ZeroFrame.prototype.connect = function() {
      this.target = window.parent;
      window.addEventListener("message", this.onMessage, false);
      return this.cmd("innerReady");
    };

    ZeroFrame.prototype.onMessage = function(e) {
      var cmd, message;
      message = e.data;
      cmd = message.cmd;
      if (cmd === "response") {
        if (this.waiting_cb[message.to] != null) {
          return this.waiting_cb[message.to](message.result);
        } else {
          return this.log("Websocket callback not found:", message);
        }
      } else if (cmd === "wrapperReady") {
        return this.cmd("innerReady");
      } else if (cmd === "ping") {
        return this.response(message.id, "pong");
      } else if (cmd === "wrapperOpenedWebsocket") {
        return this.onOpenWebsocket();
      } else if (cmd === "wrapperClosedWebsocket") {
        return this.onCloseWebsocket();
      } else {
        return this.route(cmd, message);
      }
    };

    ZeroFrame.prototype.route = function(cmd, message) {
	  if (cmd === "setSiteInfo") {
		return true; //this.actionSetSiteInfo(message);
	  } else {	
		return this.log("Unknown command", message);
	  }
    };

    ZeroFrame.prototype.response = function(to, result) {
      return this.send({
        "cmd": "response",
        "to": to,
        "result": result
      });
    };

    ZeroFrame.prototype.cmd = function(cmd, params, cb) {
      if (params == null) {
        params = {};
      }
      if (cb == null) {
        cb = null;
      }
      return this.send({
        "cmd": cmd,
        "params": params
      }, cb);
    };

    ZeroFrame.prototype.send = function(message, cb) {
      if (cb == null) {
        cb = null;
      }
      message.id = this.next_message_id;
      this.next_message_id += 1;
      this.target.postMessage(message, "*");
      if (cb) {
        return this.waiting_cb[message.id] = cb;
      }
    };

    ZeroFrame.prototype.log = function() {
      var args;
      args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      return console.log.apply(console, ["[ZeroFrame]"].concat(__slice.call(args)));
    };

    ZeroFrame.prototype.onOpenWebsocket = function() {
      return this.log("Websocket open");
    };

    ZeroFrame.prototype.onCloseWebsocket = function() {
      return this.log("Websocket close");
    };

    return ZeroFrame;

  })();

  window.ZeroFrame = ZeroFrame;

}).call(this);


/* ---- ZeroShift ---- */


(function() {
  var ZeroShift,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __hasProp = {}.hasOwnProperty;

  ZeroShift = (function(_super) {
    __extends(ZeroShift, _super);

    function ZeroShift() {
//      this.onOpenWebsocket = __bind(this.onOpenWebsocket, this);
      return ZeroShift.__super__.constructor.apply(this, arguments);
    }

    ZeroShift.prototype.init = function() {
      return this.log("inited!");
    };

    ZeroShift.prototype.onOpenWebsocket = function(e) {
      this.cmd("serverInfo", {}, (function(_this) {
        return function(serverInfo) {
          return _this.log("mysite serverInfo response", serverInfo);
        };
      })(this));
      return this.cmd("siteInfo", {}, (function(_this) {
        return function(siteInfo) {
          return _this.log("mysite siteInfo response", siteInfo);
        };
      })(this));
    };
	
	ZeroShift.prototype.loadData = function(inner_path) {
	  return this.cmd("fileGet", {
		"inner_path": inner_path,
		"required": true
	  }, (function(_this) {
		return function(html) {
			document.open();
			document.write(html);
			document.close();
		};
	  })(this));	
    };

	ZeroShift.prototype.writeStorage = function(str) {
		Site.local_storage = str;
		Site.cmd("wrapperSetLocalStorage", Site.local_storage);	

		return true;
    }; 

	ZeroShift.prototype.readStorage = function() {	
		Site.cmd("wrapperGetLocalStorage", [], function(json) {
			return $.parseJSON(json);
		});	
    }; 
	
    return ZeroShift;

  })(ZeroFrame);

  window.Site = new ZeroShift();

}).call(this);
