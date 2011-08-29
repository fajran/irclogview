function add_line_links() {
    $('.log > li').each(function() {
        var id = $(this).attr('id');
        var el = $(this).find('span.time');
        var time = el.text();
        var a = $('<a href="#'+id+'"/>');
        a.text(time);
        el.html(a);
    });
}

$(document).ready(function() {
    add_line_links();
});

