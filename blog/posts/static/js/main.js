$(document).ready(function() {
    $('.toggle-comments').click(function(e) {
        commentsUl = $(this).closest('.post').find('.comments');
        if (commentsUl.children('li').length > 0) {
            commentsUl.empty();
        } else {
            commentsUrl = $(this).attr('data-comments-url');
            $.get(commentsUrl, function(comments) {
                $.each(comments, function(index, comment) {
                    commentsUl.append('<li>' + comment.body + '</li>');
                });
            });
        }
        e.preventDefault();
    });
});
