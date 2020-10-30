$.fancybox.defaults.btnTpl.close = '<a title="{{CLOSE}}" class="fancybox-button fancybox-button--close" data-fancybox-close href="javascript:;"><i class="fas fa-times"></i></a>';
$.fancybox.defaults.btnTpl.arrowRight = '<a title="{{NEXT}}" class="fancybox-button fancybox-button--arrow_right" data-fancybox-next href="javascript:;"><i class="fas fa-arrow-right"></i></a>';
$.fancybox.defaults.btnTpl.arrowLeft = '<a title="{{PREV}}" class="fancybox-button fancybox-button--arrow_left" data-fancybox-prev href="javascript:;"><i class="fas fa-arrow-left"></i></a>';
$.fancybox.defaults.btnTpl.thumbs = '<a title="{{THUMBS}}" class="fancybox-button fancybox-button--thumbs" data-fancybox-thumbs href="javascript:;"><i class="fas fa-th"></i></a>';
$.fancybox.defaults.btnTpl.download = '<a title="{{DOWNLOAD}}" class="fancybox-button fancybox-button--download" target="_blank" data-fancybox-download href="javascript:;"><i class="fas fa-download"></i></a>';
$.fancybox.defaults.btnTpl.album = '<a title="Go to album" class="fancybox-button fancybox-button--album" target="_blank" data-fancybox-album href="javascript:;"><i class="fas fa-images"></i></a>';

$(function () {
    $(".photo-card a").fancybox({
        buttons: [
            "album",
            "download",
            "thumbs",
            "close"
        ],
        afterShow: function(instance, current) {
            $(instance.$refs.container)
              .find("[data-fancybox-download]")
              .attr("href", current.opts.download);
            if (current.opts.album) {
                $(instance.$refs.container)
                    .find("[data-fancybox-album]")
                    .attr("href", current.opts.album);
            } else {
                $(instance.$refs.container)
                    .find("[data-fancybox-album]")
                    .remove();
            }
        }
    });
});
