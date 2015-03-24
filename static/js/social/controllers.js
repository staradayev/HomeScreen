angular.module('atoControllers', [])

    .controller('CategoryCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){               
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.blocked = false;
                $scope.page = $routeParams.pageNum || 0;
                setPage("category");
                $scope.maxPage = 1;
                $scope.title = '';

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
                setPage("category");
                $scope.maxPage = 1;
                    $scope.title = $scope.trans_categories;

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
                setPage("popular");
                $scope.maxPage = 1;
                $scope.blocked = false;
                    $scope.title = $scope.trans_popular;

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
                setPage("most");
                $scope.maxPage = 1;
                $scope.blocked = false;
                    $scope.title = $scope.trans_most_rised;

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
                setPage("newest");
                $scope.maxPage = 1;
                $scope.blocked = false;

                $scope.title = $scope.trans_recently_added;

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
                setPage('search', $routeParams.searchVal);
                $scope.maxPage = 1;
                $scope.blocked = false;
                $scope.search = true;
                    $scope.title = $routeParams.searchVal;              

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
    
    .controller('SingleCtrl', ['$scope', '$routeParams', '$sce', '$window', 'atoApi',
            function($scope, $routeParams, $sce, $window, atoApi){                
                $scope.ln = $scope.current_lang || $routeParams.ln;
                setPage("photo");
                    $scope.title = $scope.trans_picture;  
                
                atoApi.getPicture($routeParams.ln, $routeParams.picId, $scope.u_email).then(function(response){
                    $scope.image = response.entity;
                });

                atoApi.getOrganizations($routeParams.ln, ($scope.is_auth) ? $scope.u_email : null).then(function(response){
                    $scope.orgs = response.entity;
                    setTimeout(function(){
                        relayout();
                    }, 100)        
                })

                $scope.like = function(pic){
                    like_picture(pic.id);
                    pic.liked = 'true';
                };

                $scope.freeStuff = function(pic){
                    window.open($scope.serverUrl+"/care/freeload/"+$scope.image.id+"/1");
                };

                $scope.setOrganization = function(org){
                    atoApi.getPayForm($routeParams.ln, org.id, $scope.image.id).then(function(response){
                        $scope.payForm = $sce.trustAsHtml(response.form);
                    });
                };

                $scope.tagSearch = function(tag){
                    window.location = $scope.serverUrl + '/social/' + $scope.ln + '/search/' + encodeURIComponent(tag.name.replace('#', ''));
                };
        }])
    
    .controller('AuthorsCtrl', ['$scope', '$routeParams', '$window', 'atoApi',
            function($scope, $routeParams, $window, atoApi){
                $scope.ln = $scope.current_lang || $routeParams.ln;
                $scope.page = $routeParams.pageNum || 0;
                setPage("photographer");
                $scope.maxPage = 1;
                $scope.blocked = false;
                    $scope.title = $scope.trans_photographers;                
                
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

                                    setTimeout(function(){
                                        init_gallery();
                                    }, 100); 
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
                setPage("photographer");
                $scope.maxPage = 1;
                $scope.blocked = false;
                $scope.photographer = {};             
                
                $scope.getNext = function(){
                    if($scope.page < $scope.maxPage){
                        $scope.blocked = true;
                        atoApi.getAuthorPictures($routeParams.ln, $routeParams.userId, $scope.page + 1).then(function(response){
                            
                            if(response.entity){
                                //first init
                                if($scope.page == 0){
                                    $scope.images = response.entity;
                                    $scope.maxPage = response.count;
                                    $scope.photographer.name = response.page_name;
                                    $scope.photographer.photo = response.author_photo;
                                    $scope.photographer.thumbnail = response.author_thumbnail;
                                    $scope.photographer.links = response.author_links;
                                    $scope.photographer.help = response.author_help;
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
            