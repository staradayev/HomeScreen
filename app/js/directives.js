'use strict';

/* Directives */


angular.module('myApp.directives', ['myApp.controllers'])
  .directive('customButton', function(){
  	return {
  		restrict: 'E',
  		replace: true,
  		scope: {
  			noteCount: "=",
  			localizedText: "="
  		},
  		templateUrl: 'templates/customButtonTemplate.html',
  		link:function(scope, element, attrs) {
  			element.addClass(attrs.type);	
  		}
  	};
  })
  .directive('news', function(){
  	return {
  		restrict: 'E',
  		replace: true,
  		templateUrl: 'templates/newsTemplate.html',
  		link: function(scope, element, attrs){
			
  		}
  	};
  }).
  directive('fastButton', function($location){
    return function(scope, elem, attr) {
        new FastButton(elem[0], function() {
          scope.$apply(function () {
            $location.path(attr.link);
          });
        });        
    };
  }).
  directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }]);
