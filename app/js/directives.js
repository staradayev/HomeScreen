'use strict';

/* Directives */


angular.module('myApp.directives', [])
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
  			element.attr("href", attrs.link);			
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
          $location.path(attrs.link);
        });

        
            //scope.$apply(attr.fastClick);
        
    };
  }).
  directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }]);
