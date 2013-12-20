'use strict';


// Declare app level module which depends on filters, and services
angular.module('Biller', [])

/* Controllers */

// Main: stores status
.controller('CtrlMain', function($scope, $http) {
	// Settings
	$scope.items = {};
	$scope.focus = 0;
	$scope.tables = [{name:'Tafel 1'}];
	$scope.count = 1;
	$scope.sum = 0;

	// Fetch items
	$http.get('cache/items.json').success(function(d){
		if(d.items){
			$scope.items = angular.copy(d.items);
		}
	});

	$scope.toggle = function(index){
		$scope.tables[index].more = !$scope.tables[index].more;
		$scope.focus = index;
		$scope.sum = $scope.tables[index].sum;
	};

	$scope.add = function(item,price){
		var t = $scope.tables[$scope.focus];
		if(!t.items){
			t.items = {};
		}
		if(!t.items[item]){
			t.items[item] = {count:1,price:price};
		}
		else {
			t.items[item].count++;
		}
		if(!t.sum) t.sum = 0;
		t.sum	+= parseFloat(price);
		t.sum = parseFloat(t.sum.toFixed(2));

		$scope.sum = t.sum;
	};

	$scope.table = function(){
		$scope.count++;
		$scope.tables.push({name:'Tafel '+$scope.count})
	};

	$scope.done = function(index){
		$scope.tables.splice(index, 1);
		$scope.sum = 0;
	};

	$scope.checkout = function(){
		console.log($scope.tables[$scope.focus])
	};
})
