angular.module('atoApp', ['ngRoute', 'atoServices', 'atoControllers', 'atoDirectives', 'infinite-scroll', 'ngSanitize'])
    .config(['$routeProvider', '$locationProvider', '$httpProvider', function($routeProvider, $locationProvider, $httpProvider){
        $routeProvider
        .when('/:ln/category/:catId', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'CategoryCtrl'
        })
        .when('/:ln/category/:catId/page/:pageNum', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'CategoryCtrl'
        })
        .when('/:ln/categories', {
            templateUrl: '/static/html/social/multiply-list.html',
            controller: 'CategoriesCtrl'
        })
        .when('/:ln/categories/page/:pageNum', {
            templateUrl: '/static/html/social/multiply-list.html',
            controller: 'CategoriesCtrl'
        })
        .when('/:ln/popular', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'PopularCtrl'
        })
        .when('/:ln/popular/page/:pageNum', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'PopularCtrl'
        })
        .when('/:ln/mostraised', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'MostRaisedCtrl'
        })
        .when('/:ln/mostraised/page/:pageNum', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'MostRaisedCtrl'
        })
        .when('/:ln/newest', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'NewestCtrl'
        })
        .when('/:ln/newest/page/:pageNum', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'NewestCtrl'
        })
        .when('/:ln/search/:searchVal', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'SearchCtrl'
        })
        .when('/:ln/search/:searchVal/page/:pageNum', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'SearchCtrl'
        })
        .when('/:ln/picture/:picId', {
            templateUrl: '/static/html/social/single.html',
            controller: 'SingleCtrl'
        })
        .when('/:ln/authors/', {
            templateUrl: '/static/html/social/authors.html',
            controller: 'AuthorsCtrl'
        })
        .when('/:ln/authors/page/:pageNum', {
            templateUrl: '/static/html/social/authors.html',
            controller: 'AuthorsCtrl'
        })
        .when('/:ln/authorpictures/:userId/', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'AuthorPicturesCtrl'
        })
        .when('/:ln/authorpictures/:userId/page/:pageNum', {
            templateUrl: '/static/html/social/multiply.html',
            controller: 'AuthorPicturesCtrl'
        })
        .otherwise({
            redirectTo: '/ua/popular'
        });

        //Remove # from url
        $locationProvider.html5Mode(true);
        
        
    }]).run(function($rootScope) {
        $rootScope.serverUrl = "http://127.0.0.1:8000"
        $rootScope.current_lang = $('#Lang_code').val();
    });

