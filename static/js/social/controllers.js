angular.module('atoControllers', [])

    .controller('CategoryCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){               
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.blocked = false;
                $scope.page = $routeParams.pageNum || 0;
                $scope.maxPage = 1;
                $scope.title = 'Category';

                $scope.getNext = function(){
                    if($scope.page < $scope.maxPage){
                        $scope.blocked = true;
                        atoApi.getCategory($routeParams.ln, $routeParams.catId, $scope.page + 1).then(function(response){
                            
                            if(response.entity){
                                //first init
                                if($scope.page == 0){
                                    $scope.images = response.entity;
                                    $scope.title = response.page_name;
                                    $scope.maxPage = response.count;
                                }else{
                                    for (var i = 0; i < response.entity.length; i++) {
                                        $scope.images.push(response.entity[i]);
                                    };
                                }
                                $scope.page = $scope.page + 1;
                                $scope.blocked = false;
                            }
                        });
                    }
                };

                $scope.getNext();
        }])
    
    .controller('CategoriesCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.blocked = false;
                $scope.page = $routeParams.pageNum || 0;
                $scope.maxPage = 1;
                if($scope.ln == 'en')
                    $scope.title = 'Categories';
                else
                    $scope.title = 'Категорії'; 

                $scope.getNext = function(){
                    if($scope.page < $scope.maxPage){
                        $scope.blocked = true;
                        atoApi.getCategories($routeParams.ln, $scope.page + 1).then(function(response){
                            
                            if(response.entity){
                                //first init
                                if($scope.page == 0){
                                    $scope.multiplies = response.entity;
                                    $scope.maxPage = response.count;
                                }else{
                                    for (var i = 0; i < response.entity.length; i++) {
                                        $scope.multiplies.push(response.entity[i]);
                                    };
                                }
                                $scope.page = $scope.page + 1;
                                $scope.blocked = false;
                            }
                        });
                    }
                };

                $scope.getNext();
        }])
    
    .controller('PopularCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){                
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.page = $routeParams.pageNum || 0;
                $scope.maxPage = 1;
                $scope.blocked = false;
                if($scope.ln == 'en')
                    $scope.title = 'Popular';
                else
                    $scope.title = 'Популярні';

                $scope.getNext = function(){
                    if($scope.page < $scope.maxPage){
                        $scope.blocked = true;
                        atoApi.getPopular($routeParams.ln, $scope.page + 1).then(function(response){
                            
                            if(response.entity){
                                //first init
                                if($scope.page == 0){
                                    $scope.images = response.entity;
                                    $scope.maxPage = response.count;
                                }else{
                                    for (var i = 0; i < response.entity.length; i++) {
                                        $scope.images.push(response.entity[i]);
                                    };
                                }

                                
                                $scope.page = $scope.page + 1;
                                $scope.blocked = false;
                            }
                        });
                    }
                };

                $scope.getNext();
        }])
    
    .controller('MostRaisedCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){                
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.page = $routeParams.pageNum || 0;
                $scope.maxPage = 1;
                $scope.blocked = false;
                if($scope.ln == 'en')
                    $scope.title = 'Most Raised';
                else
                    $scope.title = 'Найбільш Актуальні';

                $scope.getNext = function(){
                    if($scope.page < $scope.maxPage){
                        $scope.blocked = true;
                        atoApi.getMostRaised($routeParams.ln, $scope.page + 1).then(function(response){
                            
                            if(response.entity){
                                //first init
                                if($scope.page == 0){
                                    $scope.images = response.entity;
                                    $scope.maxPage = response.count;
                                }else{
                                    for (var i = 0; i < response.entity.length; i++) {
                                        $scope.images.push(response.entity[i]);
                                    };
                                }
                                $scope.page = $scope.page + 1;
                                $scope.blocked = false;
                            }
                        });
                    }
                };
                $scope.getNext();
        }])
    
    .controller('NewestCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){                
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.page = $routeParams.pageNum || 0;
                $scope.maxPage = 1;
                $scope.blocked = false;

                if($scope.ln == 'en')
                    $scope.title = 'Newest Pictures';
                else
                    $scope.title = 'Нові Зображення';

                $scope.getNext = function(){
                    if($scope.page < $scope.maxPage){
                        $scope.blocked = true;
                        atoApi.getNewest($routeParams.ln, $scope.page + 1).then(function(response){
                            
                            if(response.entity){
                                //first init
                                if($scope.page == 0){
                                    $scope.images = response.entity;
                                    $scope.maxPage = response.count;
                                }else{
                                    for (var i = 0; i < response.entity.length; i++) {
                                        $scope.images.push(response.entity[i]);
                                    };
                                }
                                $scope.page = $scope.page + 1;
                                $scope.blocked = false;
                            }
                        });
                    }
                }; $scope.getNext();
        }])
    
    .controller('SearchCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.page = $routeParams.pageNum || 0;
                $scope.maxPage = 1;
                $scope.blocked = false;
                if($scope.ln == 'en')
                    $scope.title = 'Search';
                else
                    $scope.title = 'Пошук';                

                $scope.getNext = function(){
                    if($scope.page < $scope.maxPage){
                        $scope.blocked = true;
                        atoApi.search($routeParams.ln, $routeParams.searchVal, $scope.page + 1).then(function(response){
                            
                            if(response.entity){
                                //first init
                                if($scope.page == 0){
                                    $scope.images = response.entity;
                                    $scope.maxPage = response.count;
                                }else{
                                    for (var i = 0; i < response.entity.length; i++) {
                                        $scope.images.push(response.entity[i]);
                                    };
                                }
                                $scope.page = $scope.page + 1;
                                $scope.blocked = false;
                            }
                        });
                    }
                };
                $scope.getNext();
        }])
    
    .controller('SingleCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){                
                $scope.ln = $scope.current_lang || $routeParams.ln;
                if($scope.ln == 'en')
                    $scope.title = 'Picture';
                else
                    $scope.title = 'Зображення';
                
                atoApi.getPicture($routeParams.ln, $routeParams.picId, $scope.u_email).then(function(response){
                    $scope.image = response.entity;
                });

                $scope.like = function(pic){
                    like_picture(pic.id);
                    pic.liked = 'true';
                }
        }])
    
    .controller('AuthorsCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.page = $routeParams.pageNum || 0;
                $scope.maxPage = 1;
                $scope.blocked = false;
                if($scope.ln == 'en')
                    $scope.title = 'Authors';
                else
                    $scope.title = 'Автори';                
                
                atoApi.getAuthors($routeParams.ln, $routeParams.pageNum).then(function(response){
                    $scope.photographers = response.entity;
                    //console.log($scope.photographers);
                    setTimeout(function(){
                        init_gallery();
                    }, 100); 
                });

                $scope.getNext = function(){
                    if($scope.page < $scope.maxPage){
                        $scope.blocked = true;
                        atoApi.getAuthors($routeParams.ln, $scope.page + 1).then(function(response){
                            
                            if(response.entity){
                                //first init
                                if($scope.page == 0){
                                    $scope.photographers = response.entity;
                                    $scope.maxPage = response.count;
                                    setTimeout(function(){
                                        init_gallery();
                                    }, 100); 
                                }else{
                                    for (var i = 0; i < response.entity.length; i++) {
                                        $scope.photographers.push(response.entity[i]);
                                    };
                                }
                                $scope.page = $scope.page + 1;
                                $scope.blocked = false;
                            }
                        });
                    }
                };
                $scope.getNext();
        }])
    .controller('AuthorPicturesCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.page = $routeParams.pageNum || 0;
                $scope.maxPage = 1;
                $scope.blocked = false;
                if($scope.ln == 'en')
                    $scope.title = 'Author';
                else
                    $scope.title = 'Автор';                
                
                $scope.getNext = function(){
                    if($scope.page < $scope.maxPage){
                        $scope.blocked = true;
                        atoApi.getAuthorPictures($routeParams.ln, $routeParams.userId, $scope.page + 1).then(function(response){
                            
                            if(response.entity){
                                //first init
                                if($scope.page == 0){
                                    $scope.images = response.entity;
                                    $scope.maxPage = response.count;
                                    $scope.title = response.page_name;
                                }else{
                                    for (var i = 0; i < response.entity.length; i++) {
                                        $scope.images.push(response.entity[i]);
                                    };
                                }
                                $scope.page = $scope.page + 1;
                                $scope.blocked = false;
                            }
                        });
                    }
                };
                $scope.getNext();

        }]);
            