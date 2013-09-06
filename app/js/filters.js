'use strict';

/* Filters */

angular.module('myApp.filters', ['myApp.services']).
  filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    }
  }]).
    filter('i18n', ['localize', function (localize) {
    return function (input) {
        return localize.getLocalizedString(input);
    };
}]);
