(function (window, document) {

    var layout   = document.getElementById('layout'),
        menu     = document.getElementById('menu'),
        menuLink = document.getElementById('menuLink'),
        content  = document.getElementById('main');

    function changeWeek(){
        var w = document.getElementById('week');
        var url = window.location.href;    
        if (url.indexOf('?') != -1){
            url = url.slice(0,url.indexOf('?'))
            url += '?week=' + w
        }else{
            url += '?week=' + w
        }
        window.location.href = url;
    }

    // function getData(vars) {
    //     return vars;
    // }

    // function keepParams(e){
    //     e.preventDefault();
    //     window.location='/'+window.location.search;
    // }

    function toggleClass(element, className) {
        var classes = element.className.split(/\s+/),
            length = classes.length,
            i = 0;

        for(; i < length; i++) {
          if (classes[i] === className) {
            classes.splice(i, 1);
            break;
          }
        }
        // The className is not found
        if (length === classes.length) {
            classes.push(className);
        }

        element.className = classes.join(' ');
    }

    function toggleAll(e) {
        var active = 'active';

        e.preventDefault();
        toggleClass(layout, active);
        toggleClass(menu, active);
        toggleClass(menuLink, active);
    }

    menuLink.onclick = function (e) {
        toggleAll(e);
    };

    content.onclick = function(e) {
        if (menu.className.indexOf('active') !== -1) {
            toggleAll(e);
        }
    };

}(this, this.document));