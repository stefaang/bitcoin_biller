'use strict';


// Declare app level module which depends on filters, and services
angular.module('Biller', [])
.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.useXDomain = true;
	delete $httpProvider.defaults.headers.common['X-Requested-With'];
}
])

/* Controllers */

// Main
.controller('CtrlMain', function($scope, $http, $timeout) {
	// Settings
	$scope.items = {};
	$scope.focus = 0;
	$scope.tabs = [{name:'Tab One'},{name:'Tab Two'},{name:'Tab Three'}];
	$scope.count = 1;

	$scope.print = true;
	$scope.printer = 'http://192.168.0.227';
	$scope.server = {ip:'192.168.0.227'};
	$scope.inet = {ticking:2, slowperiod:15*60*1000};

	$scope.rate = 500;
	$scope.rateMethod = 'bitpay';
	$scope.pct = 3;

	$scope.addr = '12LN7XiuegAgj9SJAxLQQwJBmiwYGTpSs9';
	$scope.txs = [];
	$scope.oldTxs = [];

	// TODO: Auth
	$scope.user = {name:'Waiter', key:'waiter'};
	$scope.copy = {};
	angular.copy($scope.user, $scope.copy);

	// Fetch items
	$http.get('cache/items.json', {timeout:5000}).success(function(d){
		var o = angular.fromJson(d);
		if(o.items){
			$scope.items = angular.copy(o.items);
		}
	});

	$scope.getRate = function(index){
		$scope.inet.update('Refreshing rate');
		$http.get('https://bitpay.com/api/rates', {timeout:5000}).success(function(d){
			var o = angular.fromJson(d);
			if(o[1].code == 'EUR'){
				$scope.rate = o[1].rate;
			}
			$scope.inet.update('Rate refreshed');
		})
		.error(function(){
			$scope.inet.update('Cannot get rate',true);
		})
	};

	$scope.mbtc = function(){
		return ($scope.tabs[$scope.focus].sum||0) * 1000 / $scope.rate * (1 - $scope.pct / 100);
	};

	$scope.archive = function(){
		$scope.oldTxs = angular.copy($scope.txs);
		$scope.updateTxs();
	};

	$scope.showall = function(){
		$scope.oldTxs = [];
		$scope.getLatest();
	};

	$scope.getLatest = function(){
		console.log('latest')
		$timeout.cancel($scope.inet.ticker);
		$scope.inet.update('Refreshing payments');
		$http.get('http://thomasg.be/biller/txs.php?a=' + $scope.addr).success(function(d){
			$scope.updateTxs(angular.fromJson(d.txs));
			$scope.inet.update('Payments refreshed');
			$scope.inet.ticker = $timeout($scope.inet.tick, 10000);
		})
		.error(function(a,b,c,d){
			console.log(a)
			console.log(b)
			console.log(c)
			$scope.inet.update('Cannot get payments',1);
			$scope.inet.ticker = $timeout($scope.inet.tick, 10000);
		})
	};

	$scope.updateTxs = function(txs){
		if(txs){
			console.log(txs)
			$scope.txs = angular.copy(txs).filter(function(tx) {
				for (var i = $scope.oldTxs.length - 1; i >= 0; i--) {
					if($scope.oldTxs[i].hash == tx.hash)
						return false;
				}
				return true;
			});
		}
		else{
			$scope.txs = [];
		}
	};

	$scope.getQr = function(amount){
		amount = amount || ($scope.mbtc()/1000).toFixed(6);
		qr.canvas({
			canvas: document.getElementById('qrcode'),
			value: 'bitcoin:' + $scope.addr + '?amount=' + amount,
			size: 10,
			background: '#eee',
		});
		console.log('bitcoin:' + $scope.addr + '?amount=' + amount)
	};
	$scope.getQr();

	$scope.toggle = function(index){
		$scope.focus = index;
		$scope.getQr();
	};

	$scope.add = function(item,price){
		var t = $scope.tabs[$scope.focus];
		if(!t.items){
			t.items = {};
			t.count = 0;
		}
		t.count++;
		if(!t.items[item]){
			t.items[item] = {count:1,price:price};
		}
		else {
			t.items[item].count++;
		}
		if(!t.sum) t.sum = 0;
		t.sum	+= parseFloat(price);
		t.sum = parseFloat(t.sum.toFixed(2));

		$scope.getQr();
	};

	$scope.tab = function(){
		$scope.count++;
		$scope.tabs.push({name:'Tafel '+$scope.count})
	};

	$scope.settle = function(index, method){
		$scope.tabs[index].method = method;
		if(!$scope.print) return;

		/* Print request */
		switch(method){
			case 'BTC':
			$scope.bitcoin(index);
			break;
			case 'Cash':
			$scope.cash(index);
			break;
			case 'Bancontact':
			$scope.bancontact(index);
			break;
			default:
			$scope.tabs[index].method = 'Payment method error';
		}
		$scope.getQr();
	};

	$scope.bitcoin = function(index){
		var t = $scope.tabs[index];
		t.class = 'alert alert-warning';
		t.status = 'Trying to print payment request';
		$http.get($scope.printer + '?a=12LN7XiuegAgj9SJAxLQQwJBmiwYGTpSs9&b=' + t.sum/1000, {timeout:5000}).success(function(d){
			t.class = 'alert alert-info';
			t.status = 'Payment request for ' + t.sum + 'mBTC printed';
		})
		.error(function() {
			t.class = 'alert alert-danger';
			t.status = 'Could not find printserver';
		});
	};

	$scope.cash = function(index){
		var t = $scope.tabs[index];
		t.class = 'alert alert-danger';
		t.status = 'Cash not implemented';
	};

	$scope.bancontact = function(index){
		var t = $scope.tabs[index];
		t.class = 'alert alert-danger';
		t.status = 'Bancontact not implemented';
	};

	$scope.settled = function(index){
		$scope.tabs[index] = {name:$scope.tabs[index].name};
		$scope.getQr();
	};

	$scope.inet.update = function(msg, error){
		$scope.inet.time = Date.now();
		$scope.inet.msg = msg;
		$scope.inet.error = error?true:false;
	};

	$scope.inet.tick = function(times){
		if(times) $scope.inet.ticking = times;
		if(!$scope.inet.ticking) return;
		$scope.inet.ticking--;
	};

	$scope.inet.check = function(){
		console.log('check')
		$scope.inet.ticking = $scope.inet.ticking?0:30;
		$scope.getLatest();
	};

	$scope.inet.slowtick = function(period){
		$scope.inet.slowperiod = period || $scope.inet.slowperiod;
		$scope.getLatest();
		$scope.getRate();
		$timeout($scope.inet.tick, $scope.inet.slowperiod);
	};
	$scope.inet.slowtick();
})


/*
 FastClick: polyfill to remove click delays on browsers with touch UIs.

 @version 0.6.7
 @codingstandard ftlabs-jsv2
 @copyright The Financial Times Limited [All Rights Reserved]
 @license MIT License (see LICENSE.txt)
 */
 function FastClick(a){var b,c=this;this.trackingClick=!1;this.trackingClickStart=0;this.targetElement=null;this.lastTouchIdentifier=this.touchStartY=this.touchStartX=0;this.layer=a;if(!a||!a.nodeType)throw new TypeError("Layer must be a document node");this.onClick=function(){return FastClick.prototype.onClick.apply(c,arguments)};this.onMouse=function(){return FastClick.prototype.onMouse.apply(c,arguments)};this.onTouchStart=function(){return FastClick.prototype.onTouchStart.apply(c,arguments)};this.onTouchEnd=
 function(){return FastClick.prototype.onTouchEnd.apply(c,arguments)};this.onTouchCancel=function(){return FastClick.prototype.onTouchCancel.apply(c,arguments)};FastClick.notNeeded(a)||(this.deviceIsAndroid&&(a.addEventListener("mouseover",this.onMouse,!0),a.addEventListener("mousedown",this.onMouse,!0),a.addEventListener("mouseup",this.onMouse,!0)),a.addEventListener("click",this.onClick,!0),a.addEventListener("touchstart",this.onTouchStart,!1),a.addEventListener("touchend",this.onTouchEnd,!1),a.addEventListener("touchcancel",
 	this.onTouchCancel,!1),Event.prototype.stopImmediatePropagation||(a.removeEventListener=function(d,b,c){var e=Node.prototype.removeEventListener;"click"===d?e.call(a,d,b.hijacked||b,c):e.call(a,d,b,c)},a.addEventListener=function(b,c,f){var e=Node.prototype.addEventListener;"click"===b?e.call(a,b,c.hijacked||(c.hijacked=function(a){a.propagationStopped||c(a)}),f):e.call(a,b,c,f)}),"function"===typeof a.onclick&&(b=a.onclick,a.addEventListener("click",function(a){b(a)},!1),a.onclick=null))}
 FastClick.prototype.deviceIsAndroid=0<navigator.userAgent.indexOf("Android");FastClick.prototype.deviceIsIOS=/iP(ad|hone|od)/.test(navigator.userAgent);FastClick.prototype.deviceIsIOS4=FastClick.prototype.deviceIsIOS&&/OS 4_\d(_\d)?/.test(navigator.userAgent);FastClick.prototype.deviceIsIOSWithBadTarget=FastClick.prototype.deviceIsIOS&&/OS ([6-9]|\d{2})_\d/.test(navigator.userAgent);
 FastClick.prototype.needsClick=function(a){switch(a.nodeName.toLowerCase()){case "button":case "select":case "textarea":if(a.disabled)return!0;break;case "input":if(this.deviceIsIOS&&"file"===a.type||a.disabled)return!0;break;case "label":case "video":return!0}return/\bneedsclick\b/.test(a.className)};
 FastClick.prototype.needsFocus=function(a){switch(a.nodeName.toLowerCase()){case "textarea":case "select":return!0;case "input":switch(a.type){case "button":case "checkbox":case "file":case "image":case "radio":case "submit":return!1}return!a.disabled&&!a.readOnly;default:return/\bneedsfocus\b/.test(a.className)}};
 FastClick.prototype.sendClick=function(a,b){var c,d;document.activeElement&&document.activeElement!==a&&document.activeElement.blur();d=b.changedTouches[0];c=document.createEvent("MouseEvents");c.initMouseEvent("click",!0,!0,window,1,d.screenX,d.screenY,d.clientX,d.clientY,!1,!1,!1,!1,0,null);c.forwardedTouchEvent=!0;a.dispatchEvent(c)};FastClick.prototype.focus=function(a){var b;this.deviceIsIOS&&a.setSelectionRange?(b=a.value.length,a.setSelectionRange(b,b)):a.focus()};
 FastClick.prototype.updateScrollParent=function(a){var b,c;b=a.fastClickScrollParent;if(!b||!b.contains(a)){c=a;do{if(c.scrollHeight>c.offsetHeight){b=c;a.fastClickScrollParent=c;break}c=c.parentElement}while(c)}b&&(b.fastClickLastScrollTop=b.scrollTop)};FastClick.prototype.getTargetElementFromEventTarget=function(a){return a.nodeType===Node.TEXT_NODE?a.parentNode:a};
 FastClick.prototype.onTouchStart=function(a){var b,c,d;if(1<a.targetTouches.length)return!0;b=this.getTargetElementFromEventTarget(a.target);c=a.targetTouches[0];if(this.deviceIsIOS){d=window.getSelection();if(d.rangeCount&&!d.isCollapsed)return!0;if(!this.deviceIsIOS4){if(c.identifier===this.lastTouchIdentifier)return a.preventDefault(),!1;this.lastTouchIdentifier=c.identifier;this.updateScrollParent(b)}}this.trackingClick=!0;this.trackingClickStart=a.timeStamp;this.targetElement=b;this.touchStartX=
 c.pageX;this.touchStartY=c.pageY;200>a.timeStamp-this.lastClickTime&&a.preventDefault();return!0};FastClick.prototype.touchHasMoved=function(a){a=a.changedTouches[0];return 10<Math.abs(a.pageX-this.touchStartX)||10<Math.abs(a.pageY-this.touchStartY)?!0:!1};FastClick.prototype.findControl=function(a){return void 0!==a.control?a.control:a.htmlFor?document.getElementById(a.htmlFor):a.querySelector("button, input:not([type=hidden]), keygen, meter, output, progress, select, textarea")};
 FastClick.prototype.onTouchEnd=function(a){var b,c,d;d=this.targetElement;this.touchHasMoved(a)&&(this.trackingClick=!1,this.targetElement=null);if(!this.trackingClick)return!0;if(200>a.timeStamp-this.lastClickTime)return this.cancelNextClick=!0;this.lastClickTime=a.timeStamp;b=this.trackingClickStart;this.trackingClick=!1;this.trackingClickStart=0;this.deviceIsIOSWithBadTarget&&(d=a.changedTouches[0],d=document.elementFromPoint(d.pageX-window.pageXOffset,d.pageY-window.pageYOffset));c=d.tagName.toLowerCase();
 	if("label"===c){if(b=this.findControl(d)){this.focus(d);if(this.deviceIsAndroid)return!1;d=b}}else if(this.needsFocus(d)){if(100<a.timeStamp-b||this.deviceIsIOS&&window.top!==window&&"input"===c)return this.targetElement=null,!1;this.focus(d);if(!this.deviceIsIOS4||"select"!==c)this.targetElement=null,a.preventDefault();return!1}if(this.deviceIsIOS&&!this.deviceIsIOS4&&(b=d.fastClickScrollParent)&&b.fastClickLastScrollTop!==b.scrollTop)return!0;this.needsClick(d)||(a.preventDefault(),this.sendClick(d,
 		a));return!1};FastClick.prototype.onTouchCancel=function(){this.trackingClick=!1;this.targetElement=null};FastClick.prototype.onMouse=function(a){return!this.targetElement||a.forwardedTouchEvent||!a.cancelable?!0:!this.needsClick(this.targetElement)||this.cancelNextClick?(a.stopImmediatePropagation?a.stopImmediatePropagation():a.propagationStopped=!0,a.stopPropagation(),a.preventDefault(),!1):!0};
 	FastClick.prototype.onClick=function(a){if(this.trackingClick)return this.targetElement=null,this.trackingClick=!1,!0;if("submit"===a.target.type&&0===a.detail)return!0;a=this.onMouse(a);a||(this.targetElement=null);return a};
 	FastClick.prototype.destroy=function(){var a=this.layer;this.deviceIsAndroid&&(a.removeEventListener("mouseover",this.onMouse,!0),a.removeEventListener("mousedown",this.onMouse,!0),a.removeEventListener("mouseup",this.onMouse,!0));a.removeEventListener("click",this.onClick,!0);a.removeEventListener("touchstart",this.onTouchStart,!1);a.removeEventListener("touchend",this.onTouchEnd,!1);a.removeEventListener("touchcancel",this.onTouchCancel,!1)};
 	FastClick.notNeeded=function(a){var b;if("undefined"===typeof window.ontouchstart)return!0;if(/Chrome\/[0-9]+/.test(navigator.userAgent))if(FastClick.prototype.deviceIsAndroid){if((b=document.querySelector("meta[name=viewport]"))&&-1!==b.content.indexOf("user-scalable=no"))return!0}else return!0;return"none"===a.style.msTouchAction?!0:!1};FastClick.attach=function(a){return new FastClick(a)};
 	"undefined"!==typeof define&&define.amd?define(function(){return FastClick}):"undefined"!==typeof module&&module.exports?(module.exports=FastClick.attach,module.exports.FastClick=FastClick):window.FastClick=FastClick;

 	angular.element(document).ready(function () {
 		FastClick.attach(document.body);
 	});