function add_line_links() {
    $('.log > li').each(function() {
        var id = $(this).attr('id');
        var el = $(this).find('span.time');
        var time = el.text();
        var a = $('<a href="#'+id+'"/>');
        a.text(time);
        el.html(a);

        a.click((function(line) {
            return function() {
                var el = $(line);
                if (el.hasClass('active')) {
                    el.removeClass('active');
                }
                else {
                    $('.log > li').removeClass('active');
                    el.addClass('active');
                }
                return false;
            }
        })(this));
    });
}

$(document).ready(function() {
    add_line_links();
});

