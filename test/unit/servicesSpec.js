'use strict';

/* jasmine specs for services go here */

describe('service', function() {
  beforeEach(module('myApp.services'));


  describe('version', function() {
    it('should return current version', inject(function(version) {
      expect(version).toEqual('0.1');
    }));
  });


  describe('logInUser test', function(){
  		var logIn;
  		var scope;
  		var httpBackend;

	  	beforeEach(function($rootscope){
	  		
	  		module('myApp.services');            

	  		inject(function($httpBackend, _$rootScope_, logInUser){
	  			logIn = logInUser;
	  			httpBackend = $httpBackend;
	  			scope = _$rootScope_; 
	  		});

	  		httpBackend.when('POST', 'http://192.168.144.178:8085/development/api/login').respond({ "session" : "right"});

	  	});

	  	//make sure no expectations were missed in your tests.
  		//(e.g. expectGET or expectPOST)
	  	afterEach(function() {
		    httpBackend.verifyNoOutstandingExpectation();
		    httpBackend.verifyNoOutstandingRequest();
		  });

	  	it('should be a function', inject(function(logInUser){
	  		expect(angular.isFunction(logIn.makeAsyncCall)).toBe(true);
	  	}));

	  	it('should send log and pin data and return the response.', function (){
	  		spyOn(scope, '$broadcast');
	  		httpBackend.expectPOST('http://192.168.144.178:8085/development/api/login');
	  		logIn.makeAsyncCall(scope);
	  		httpBackend.flush();
	  		expect(scope.$broadcast).toHaveBeenCalledWith('asyncLoginResult', "right");
	  	});	  	
  });


  describe('checkForMessages test', function(){
  		var checkMessages;
  		var scope;
  		var httpBackend;

	  	beforeEach(function($rootscope){
	  		
	  		module('myApp.services');

	  		inject(function($httpBackend, _$rootScope_, checkForMessages){
	  			checkMessages = checkForMessages;
	  			httpBackend = $httpBackend;
	  			scope = _$rootScope_; 
	  		});

	  		httpBackend.when('GET', 'http://192.168.144.178:8085/development/api/messages/count').respond("ActualCount");
	  	});

	  	afterEach(function() {
		    httpBackend.verifyNoOutstandingExpectation();
		    httpBackend.verifyNoOutstandingRequest();
		  });

	  	it('should be a function', inject(function(checkForMessages){
	  		expect(angular.isFunction(checkMessages.makeAsyncCall)).toBe(true);
	  	}));

	  	it('should do <<get>> request and get the response.', function (){
	  		spyOn(scope, '$broadcast');
	  		httpBackend.expectGET('http://192.168.144.178:8085/development/api/messages/count');
	  		checkMessages.makeAsyncCall(scope);
	  		httpBackend.flush();
	  		expect(scope.$broadcast).toHaveBeenCalledWith('asyncMessagesResult', "ActualCount");
	  	});	  	
  });

  describe('checkForVisits test', function(){
  		var checkVisits;
  		var scope;
  		var httpBackend;
  		var fromToDate

	  	beforeEach(function($rootscope){
	  		
	  		module('myApp.services');

	  		inject(function($httpBackend, _$rootScope_, checkForVisits){
	  			checkVisits = checkForVisits;
	  			httpBackend = $httpBackend;
	  			scope = _$rootScope_; 
	  		});

	  		var d = new Date();
            fromToDate = (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();        

	  		httpBackend.when('GET', 'http://192.168.144.178:8085/development/api/visit?FromDate=' + fromToDate + "&ToDate=" + fromToDate)
	  		.respond("visits");

	  	});

	  	it('should be a function', inject(function(checkForVisits){
	  		expect(angular.isFunction(checkVisits.makeAsyncCall)).toBe(true);
	  	}));

	  	it('should do <<get>> request and get the response.', function (){
	  		spyOn(scope, '$broadcast');
	  		httpBackend.expectGET('http://192.168.144.178:8085/development/api/visit?FromDate=' + fromToDate + "&ToDate=" + fromToDate);
	  		checkVisits.makeAsyncCall(scope);
	  		httpBackend.flush();
	  		expect(scope.$broadcast).toHaveBeenCalledWith("asyncVisitsResult", "visits");
	  	});	  
  });

describe('localize test', function(){
  		var localizeText;
  		var scope;
  		var httpBackend;
  		var url;

	  	beforeEach(function($rootscope, $provide){
	  		
	  		module('myApp.services');            

	  		inject(function($httpBackend, _$rootScope_, localize){
	  			localizeText = localize;
	  			httpBackend = $httpBackend;
	  			scope = _$rootScope_; 
	  		});
	  		url = 'i18n/resources-locale_en-US.js';
	  		httpBackend.when('GET', url).respond('WEE!');

	  	});

	  	//make sure no expectations were missed in your tests.
  		//(e.g. expectGET or expectPOST)
	  	afterEach(function() {
		    httpBackend.verifyNoOutstandingExpectation();
		    httpBackend.verifyNoOutstandingRequest();
		  });

	  	it('successCallback should be a function', inject(function(localize){
	  		expect(angular.isFunction(localizeText.successCallback)).toBe(true);
	  	}));

	  	it('initLocalizedResources should be a function', inject(function(localize){
	  		expect(angular.isFunction(localizeText.initLocalizedResources)).toBe(true);
	  	}));

	  	it('getLocalizedString should be a function', inject(function(localize){
	  		expect(angular.isFunction(localizeText.getLocalizedString)).toBe(true);
	  	}));

	  	it('localizeText should do somthing and fire broadcast localizeResourcesUpdates', function (){
	  		spyOn(scope, '$broadcast');	 
	  		localizeText.successCallback(scope);
	  		expect(scope.$broadcast).toHaveBeenCalledWith('localizeResourcesUpdates');
	  	});	 

	  	it('initLocalizedResources should get localize file, after success call successCallback', function (){
	  		spyOn(localizeText, 'successCallback').andCallThrough();	 
	  		httpBackend.expectGET(url);
	  		localizeText.initLocalizedResources();
	  		httpBackend.flush();
	  		expect(localizeText.successCallback).toHaveBeenCalled();
	  	});	  

	  	it('getLocalizedString should try get localize file, after error call initLocalizedResources', function (){
	  		spyOn(localizeText, 'initLocalizedResources').andCallThrough();	 
	  		localizeText.getLocalizedString();
	  		httpBackend.flush();
	  		expect(localizeText.initLocalizedResources).toHaveBeenCalled();
	  	});		
  });

});
