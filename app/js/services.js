'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('myApp.services', ['ngCookies', 'angular-cache']).
  value('version', '0.1')
  .factory('logInUser', ['$http', '$cookies', '$rootScope', function($http, $cookies, $rootScope) {

        var service = {
        makeAsyncCall: function (theScope) {

            $http.defaults.useXDomain = true;
            $http.defaults.withCredentials = true;
            delete $http.defaults.headers.common['X-Requested-With'];
            
            $http({method: 'POST', url: 'http://192.168.144.178:8085/development/api/login', data: { UserId: "174669", Pin: "8557" }})
            .success(function(data, status, headers, config) {
                    theScope.$broadcast('asyncLoginResult', data.session);                    
                  }).
            error(function(data, status, headers, config) {
                    theScope.$broadcast('asyncLoginResult', null); 
                  });
        }
    };
    return service;        
}
])
  .factory('checkForMessages', ['$http', '$rootScope', '$cookies', function($http, $rootScope, $cookies) {

        var service = {
        makeAsyncCall: function (theScope) {

            $http.defaults.useXDomain = true;
            delete $http.defaults.headers.common['X-Requested-With'];
            $http.defaults.withCredentials = true;
            
            $http({method: 'GET', url: 'http://192.168.144.178:8085/development/api/messages/count', headers: {'X-Addus-Uuid': $cookies.uid}})
            .success(function(data, status, headers, config) {
                    theScope.$broadcast('asyncMessagesResult', data);                    
                  }).
            error(function(data, status, headers, config) {
                    theScope.$broadcast('asyncMessagesResult', null); 
                  });
        }
    };
    return service;        
}
])
  .factory('getMessagesList', ['$http', '$rootScope', '$cookies', '$angularCacheFactory', '$q', function($http, $rootScope, $cookies, $angularCacheFactory, $q) {

        var service = {
        makeAsyncCall: function (theScope) {
            debugger;
            var deferred = $q.defer();

            if(!$angularCacheFactory.get('defaultCache')){
                $angularCacheFactory('defaultCache', {
                    maxAge: 90000, // Items added to this cache expire after 15 minutes.
                    cacheFlushInterval: 600000, // This cache will clear itself every hour.
                    aggressiveDelete: true, // Items will be deleted from this cache right when they expire.
                    storageMode: 'localStorage' // This cache will sync itself with localStorage.

                });
            }

            var messagesCache = $angularCacheFactory.get('defaultCache');
            var data = messagesCache.get("messages");

            if (data) {
                deferred.resolve(data);                                
            } else {
                $http.defaults.useXDomain = true;
                delete $http.defaults.headers.common['X-Requested-With'];
                $http.defaults.withCredentials = true;
                
                $http({method: 'GET', url: 'http://192.168.144.178:8085/development/api/messages/list', headers: {'X-Addus-Uuid': $cookies.uid}, cache: true})
                .success(function(data, status, headers, config) {
                        messagesCache.put("messages", data);
                        deferred.resolve(data);                                          
                      }).
                error(function(data, status, headers, config) {
                        deferred.resolve(null);  
                      });
            }
            return deferred.promise;
        }
    };
    return service;        
}
])
  .factory('checkForVisits', ['$http', '$rootScope', '$cookies', function($http, $rootScope, $cookies) {

        var service = {
        makeAsyncCall: function (theScope) {

            var d = new Date();
            var fromToDate = (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();          

            $http.defaults.useXDomain = true;
            delete $http.defaults.headers.common['X-Requested-With'];

            $http({method: 'GET', url: 'http://192.168.144.178:8085/development/api/visit?FromDate=' + fromToDate + "&ToDate=" + fromToDate, 
                headers: {'X-Addus-Uuid': $cookies.uid}})
            .success(function(data, status, headers, config) {
                    theScope.$broadcast('asyncVisitsResult', data);                    
                  }).
            error(function(data, status, headers, config) {
                    theScope.$broadcast('asyncVisitsResult', null); 
                  });
        }
    };
    return service;        
}
]).
factory('localize', ['$http', '$rootScope', '$window', '$filter', '$location', function ($http, $rootScope, $window, $filter, $location) {
    var localize = {
        language: $window.navigator.userLanguage || $window.navigator.language,//"ru-RU",
        dictionary:[],
        resourceFileLoaded:false,

        successCallback:function (data) {          
            localize.dictionary = data;
            localize.resourceFileLoaded = true;
            $rootScope.$broadcast('localizeResourcesUpdates');
        },

        initLocalizedResources:function () {
            $location.path();
            var url = 'i18n/resources-locale_' + localize.language + '.js';
            // request the resource file
            $http({ method:"GET", url:url, cache:false }).success(localize.successCallback).error(function () {
                // the request failed set the url to the default resource file
                var url = 'i18n/resources-locale_default.js';http://codingsmackdown.tv/?p=104&preview=true
                // request the default resource file
                $http({ method:"GET", url:url, cache:false }).success(localize.successCallback);
            });
        },

        getLocalizedString:function (value) {
            // default the result to an empty string
            var result = '';
            // check to see if the resource file has been loaded
            if (!localize.resourceFileLoaded) {
                // call the init method
                localize.initLocalizedResources();
                // set the flag to keep from looping in init
                localize.resourceFileLoaded = true;
                // return the empty string
                return result;
            }
            // make sure the dictionary has valid data
            if ((localize.dictionary !== []) && (localize.dictionary.length > 0)) {
                // use the filter service to only return those entries which match the value
                // and only take the first result
                var entry = $filter('filter')(localize.dictionary, {key:value})[0];
                // check to make sure we have a valid entry
                if ((entry !== null) && (entry != undefined)) {
                    // set the result
                    result = entry.value;
                }
            }
            // return the value to the call
            return result;
        }
    };
    // return the local instance when called
    return localize;
} ]);