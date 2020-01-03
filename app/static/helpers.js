// helpers.js

function loadMore(btn) {
    var selector = '#' + btn.id + ' p[style*="display: none"]'
    var hiddenNodes = document.querySelectorAll(selector);
    var i;
    for ( i = 0; i < 5; i++ ) {
        if ( hiddenNodes[i] !== undefined ) {
             hiddenNodes[i].style.display = 'block';
        }
    }
}
