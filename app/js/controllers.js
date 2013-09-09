'use strict';

/* Controllers */

angular.module('myApp.controllers', ['ngCookies']).
  controller('HomeScreenCtrl', ['$scope', '$cookies', '$location', 'logInUser', 'checkForMessages', 'checkForVisits', function($scope, $cookies, $location, logInUser, checkForMessages, checkForVisits) {

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
  
  .controller('MessagesCtrl', ['$scope', 'getMessagesList', function($scope, getMessagesList) {
      $scope.messages = [];

      getMessagesList.makeAsyncCall($scope).then(function(data) {
      if(data){
          $scope.unsortedMessages = data;
          $scope.sortMessages($scope.unsortedMessages);
        }
      });

      $scope.sortMessages = function(messagesUnSorted)
      {
        if(!messagesUnSorted || messagesUnSorted.length < 1)
        {
          return;
        }else{
          messagesUnSorted.reverse();
          var days = ['Saturday', 'Sunday','Monday','Tuesday','Wednesday','Thursday','Friday'];
          angular.forEach(messagesUnSorted, function(mes) {
            //If first iteration of foreach
            if($scope.messages.length < 1){             
              var dateParts = mes.DateSentText.split("/");
              var date = new Date();date.setMonth(dateParts[0]); 
              date.setDate(dateParts[1] - 1);date.setFullYear(dateParts[2]);              
              $scope.messages.push({"dateSortable":mes.DateSentSortable, 
                                    "date":mes.DateSentText,
                                    "day":days[date.getDay()],
                                    "items":[]});
              $scope.messages[0].items.push(mes);
            }else{
              //if current message has similar date publication as previous message
              if($scope.messages[$scope.messages.length-1].dateSortable == mes.DateSentSortable)
              {
                $scope.messages[$scope.messages.length-1].items.push(mes);
              }else{
                 var dateParts = mes.DateSentText.split("/");
                 var date = new Date();date.setMonth(dateParts[0]); 
                 date.setDate(dateParts[1] - 1);date.setFullYear(dateParts[2]);   
                $scope.messages.push({"dateSortable":mes.DateSentSortable, 
                                    "date":mes.DateSentText,
                                    "day":days[date.getDay()],
                                    "items":[]});
                $scope.messages[$scope.messages.length-1].items.push(mes);
              }
            }
          });
        }

      }

  }])
  
  .controller('VisitsCtrl', ['$scope', '$routeParams',function($scope, $routeParams) {
  	$scope.visit = $routeParams.VisitId;
  }])

  .controller('ScheduleCtrl', [function() {

  }])

  .controller('ScheduleAvailableCtrl', [function() {

  }])

  .controller('UserCtrl', [function() {

  }])

  .controller('PayrollCtrl', [function() {

  }])

  .controller('AnotherCtrl', [function() {

  }]);

  