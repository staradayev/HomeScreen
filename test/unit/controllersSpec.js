'use strict';

/* jasmine specs for controllers go here */

describe('controllers', function(){
	var scope;
	var homeCtrl;
	var data;

	var mockService = {
	    makeAsyncCall: function (x){
	      return 'weee';
	    }
	  }
 
  beforeEach(function(){
	  		
	  		module('myApp.controllers');

	  		inject(function(_$rootScope_, $controller, $cookies){
	  			scope = _$rootScope_; 

	  			homeCtrl = $controller('HomeScreenCtrl', {
			      $scope: scope,
			      $cookies: $cookies, 
			      logInUser : mockService, 
			      checkForMessages : mockService, 
			      checkForVisits : mockService
			    });
	  		});

	  		data = {"SessionId":"111"};
	  		
	  	});


  it('checkForMessages should be a function', inject(function() {
   expect(angular.isFunction(scope.checkForMessages)).toBe(true);
  }));

  it('the messages should be null', inject(function() {
    expect(scope.messages).toEqual(null);
  }));

  it('checkForMessages should return current scope.messages count', inject(function() {
  	scope.messages = 24;
    expect(scope.checkForMessages()).toEqual(24);
  }));

  it('asyncVisitsResult should set scope.visits', inject(function() {
	scope.$broadcast('asyncVisitsResult', "visit!");
    expect(scope.visits).toEqual("visit!");
  }));

  it('asyncMessagesResult should set scope.messages', inject(function() {
	scope.$broadcast('asyncMessagesResult', {"UnreadCount":"none"});
    expect(scope.messages).toEqual("none");
  }));

  it('asyncLoginResult should set scope.session', inject(function() {
	scope.$broadcast('asyncLoginResult', data);
    expect(scope.session).toEqual(data);
  }));
  
});
