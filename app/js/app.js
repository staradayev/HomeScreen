'use strict';


// Declare app level module which depends on filters, and services
angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives', 'myApp.controllers']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/view1', {templateUrl: 'partials/homeScreenView.html', controller: 'HomeScreenCtrl'});
    $routeProvider.when('/messages', {templateUrl: 'partials/messageView.html', controller: 'MessagesCtrl'});
    $routeProvider.when('/visits/:VisitId', {templateUrl: 'partials/visitsView.html', controller: 'VisitsCtrl'});
    $routeProvider.when('/schedule', {templateUrl: 'partials/scheduleView.html', controller: 'ScheduleCtrl'});
    $routeProvider.when('/schedule/available', {templateUrl: 'partials/availableScheduleView.html', controller: 'ScheduleAvailableCtrl'});
    $routeProvider.when('/user', {templateUrl: 'partials/userView.html', controller: 'UserCtrl'});
    $routeProvider.when('/payroll', {templateUrl: 'partials/payrollView.html', controller: 'PayrollCtrl'});
    $routeProvider.otherwise({redirectTo: '/view1'});
  }]);
