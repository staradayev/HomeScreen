'use strict';

/* Controllers */

angular.module('myApp.controllers', ['ngCookies']).
  controller('HomeScreenCtrl', ['$scope', '$cookies', 'logInUser', 'checkForMessages', 'checkForVisits', function($scope, $cookies, logInUser, checkForMessages, checkForVisits) {

	$scope.messages = null;

  	$scope.$on('asyncLoginResult', function (event, data) {
        $scope.session = data;
        if(data){
        	$cookies.uid = data.SessionId;
    	}
        checkForMessages.makeAsyncCall($scope);
        checkForVisits.makeAsyncCall($scope);
    });

    $scope.$on('asyncMessagesResult', function (event, data) {
    	if(data){
    		$scope.messages = data.UnreadCount;
    	}
    });

    $scope.$on('asyncVisitsResult', function (event, data) {
    	if(data){
    		$scope.visits = data;
    	}
    });

  	logInUser.makeAsyncCall($scope);

  	$scope.checkForMessages = function() {
  		return $scope.messages;
  	}  	
  	
  }])
  
  .controller('MessagesCtrl', [function() {

  }])
  
  .controller('VisitsCtrl', ['$scope', '$routeParams',function($scope, $routeParams) {
  	$scope.visit = $routeParams.VisitId;
  }])

  .controller('AnotherCtrl', [function() {

  }]);