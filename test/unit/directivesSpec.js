'use strict';

/* jasmine specs for directives go here */

describe('directives', function() {
  beforeEach(module('myApp.directives'));

  describe('app-version', function() {
    it('should print current version', function() {
      module(function($provide) {
        $provide.value('version', 'TEST_VER');
      });
      inject(function($compile, $rootScope) {
        var element = $compile('<span app-version></span>')($rootScope);
        expect(element.text()).toEqual('TEST_VER');
      });
    });
  });

  describe('customButton', function() {
    var $compile;
    var $rootScope;
    var elm;
 
    // Load the myApp module, which contains the directive
    beforeEach(module('myApp.directives'));
 
    // Store references to $rootScope and $compile
    // so they are available to all tests in this describe block
    beforeEach(inject(function(_$compile_, _$rootScope_){
      // The injector unwraps the underscores (_) from around the parameter names when matching
      $compile = _$compile_;
      $rootScope = _$rootScope_;
      $rootScope.noteCount = 5;
      $rootScope.localizedText = "LocaleMe";
      elm = $compile("<a class='button ico' href=''><span>"+
                          "<span class='count' id='msg-count' ng-class='{displayMessages: noteCount > 0}'>{{noteCount}}</span>"+ 
                        "</span>"+
                        "{{localizedText}}"+
                      "</a>")($rootScope);
        // fire all the watches, so the scope expression {{1 + 1}} will be evaluated
        $rootScope.$digest();
    }));
    
    it('Check if messages count right', function() {
        var spans = elm.find('span');

        expect(spans.length).toBe(2);
        expect(spans.eq(0).text()).toBe("5");
    });

    it('Check if localized Text added', function() {
        expect(elm.text()).toBe("5LocaleMe");
    });

    it('Check if messages displayed', function() {
        var spans = elm.find('span');
        expect(spans.eq(1).hasClass('displayMessages')).toBe(true);
    });

  });

  describe('news', function() {
    var $compile;
    var $rootScope;
    var elm;
 
    // Load the myApp module, which contains the directive
    beforeEach(module('myApp.directives'));
 
    // Store references to $rootScope and $compile
    // so they are available to all tests in this describe block
    beforeEach(inject(function(_$compile_, _$rootScope_){
      // The injector unwraps the underscores (_) from around the parameter names when matching
      $compile = _$compile_;
      $rootScope = _$rootScope_;
      $rootScope.curVisit = {
        "OrdSys":"12345",
        "VisitDes":"New visit",
        "ClientDes":"Client"};
      elm = $compile("<article class='list' data-id='{{curVisit.OrdSys}}'>"
                      +"<a class='running-late' data-id='{{curVisit.OrdSys}}'' href='#/visits/{{curVisit.OrdSys}}''>&nbsp;</a>"
                      +"<p><span class='ico-small time'></span>{{curVisit.VisitDes}}</p>"
                      +"<p class='client'><span class='ico-small face'></span>{{curVisit.ClientDes}}</p>"
                  +"</article>")($rootScope);
        // fire all the watches, so the scope expression {{1 + 1}} will be evaluated
        $rootScope.$digest();
    }));
    
    it('Check if visit description right', function() {
        var article = elm.find('p');
        expect(article.eq(0).text()).toBe("New visit");
    });

    it('Check if client description right', function() {
        var article = elm.find('p');
        expect(article.eq(1).text()).toBe("Client");
    });
    it('Check if link contains id', function() {
        var article = elm.find('a');
        expect(article.attr('href')).toContain("12345");
    });

  });

});
