angular.module('atoDirectives', [])
        
    .directive('backBtn', ['$window',
        function($window){
            return {
                restrict: 'A',
                link: function ($scope, elem, attrs) {
                    elem.bind('click', function (e) {
                        e.preventDefault();
                        $window.history.back();
                    });
                }
            };
        }])
    
    .directive('localBtns', ['$routeParams', '$location',
        function($routeParams, $location){
            return {
                restrict: 'A',
                link: function ($scope, elem, attrs) {
                    var currentUrl = $location.$$path.replace('/'+$routeParams.ln+'/', '/');
                    
                    var links = '<li><a href="#/ua'+currentUrl+'">УКР</a></li><li><a href="#/en'+currentUrl+'">EN</a></li>'
                    
                    elem.html(links);
                }
            };
        }])
    
    .directive('searchBtn', ['$routeParams', '$location',
        function($routeParams, $location){
            return {
                restrict: 'A',
                link: function ($scope, elem, attrs) {
                    elem.bind('click', function (e) {
                        e.preventDefault();
                        
                        if($scope.searchLine)
                            $location.path($routeParams.ln+'/search/'+$scope.searchLine);
                        else
                            $location.path($routeParams.ln+'/popular');
                        
                        $scope.$apply();
                    });
                }
            };
        }]);
