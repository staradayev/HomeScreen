angular.module('atoServices', [])
    .factory('atoApi', ['$http', '$q', function($http, $q){
        var factory = {},
            apiUrl = 'http://127.0.0.1:8000/api/';
        
        factory.getPicture = function(ln, id, u_email){
            if(!id)
                return;
            
            var deffered = $q.defer();
            
            ln = ln || 'ua';
            var url = (u_email) ? apiUrl+'picture?ln='+ln+'&id='+id+'&user_id='+u_email : apiUrl+'picture?ln='+ln+'&id='+id;

            
            $http.get(url)
                .success(function(data){
                    deffered.resolve(data);
                })
                .error(function(){});
        
            return deffered.promise;
        };
        
        factory.getCategory = function(ln, id, page){
            var deffered = $q.defer();
            
            if(!id)
                return;
            
            ln = ln || 'ua';
            page = page || 1;
            $http.get(apiUrl+'catpictures?ln='+ln+'&id='+id+'&page='+page)
                .success(function(data){
                    deffered.resolve(data);
                })
                .error(function(){});
        
            return deffered.promise;
        };
        
        factory.getCategories = function(ln, page){
            var deffered = $q.defer();
            
            ln = ln || 'ua';
            page = page || 1;
            
            $http.get(apiUrl+'categories?ln='+ln+'&page='+page)
                .success(function(data){
                    deffered.resolve(data);
                })
                .error(function(){});
        
            return deffered.promise;
        };
        
        factory.getPopular = function(ln, page){
            var deffered = $q.defer();
            
            ln = ln || 'ua';
            page = page || 1;
            
            $http.get(apiUrl+'popular?ln='+ln+'&page='+page)
                .success(function(data){
                    deffered.resolve(data);
                })
                .error(function(){});
        
            return deffered.promise;
        };
        
        factory.getMostRaised = function(ln, page){
            var deffered = $q.defer();
            
            ln = ln || 'ua';
            page = page || 1;
            
            $http.get(apiUrl+'mostraised?ln='+ln+'&page='+page)
                .success(function(data){
                    deffered.resolve(data);
                })
                .error(function(){});
        
            return deffered.promise;
        };
        
        factory.getNewest = function(ln, page){
            var deffered = $q.defer();
            
            ln = ln || 'ua';
            page = page || 1;
            
            $http.get(apiUrl+'newest?ln='+ln+'&page='+page)
                .success(function(data){
                    deffered.resolve(data);
                })
                .error(function(){});
        
            return deffered.promise;
        };
        
        factory.search = function(ln, searchVal, page){            
            if(!searchVal)
                return;
            
            var deffered = $q.defer();
            
            ln = ln || 'ua';
            page = page || 1;
            
            $http.get(apiUrl+'search?ln='+ln+'&param='+searchVal+'&page='+page)
                .success(function(data){
                    deffered.resolve(data);
                })
                .error(function(){});
        
            return deffered.promise;
        };
        
        factory.getAuthors = function(ln, page){
            var deffered = $q.defer();
            
            ln = ln || 'ua';
            page = page || 1;
            
            $http.get(apiUrl+'photographers?ln='+ln+'&page='+page)
                .success(function(data){
                    deffered.resolve(data);
                })
                .error(function(){});
        
            return deffered.promise;
        };

        factory.getAuthorPictures = function(ln, id, page){
            if(!id)
                return;
            
            var deffered = $q.defer();
            
            ln = ln || 'ua';
            page = page || 1;
            
            $http.get(apiUrl+'author?ln='+ln+'&id='+id+'&page='+page)
                .success(function(data){
                    deffered.resolve(data);
                })
                .error(function(){});
        
            return deffered.promise;
        };

        return factory;
    }]);