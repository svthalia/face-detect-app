$.fancybox.defaults.btnTpl.close = '<a title="{{CLOSE}}" class="fancybox-button fancybox-button--close" data-fancybox-close href="javascript:;"><i class="fas fa-times"></i></a>';
$.fancybox.defaults.btnTpl.arrowRight = '<a title="{{NEXT}}" class="fancybox-button fancybox-button--arrow_right" data-fancybox-next href="javascript:;"><i class="fas fa-arrow-right"></i></a>';
$.fancybox.defaults.btnTpl.arrowLeft = '<a title="{{PREV}}" class="fancybox-button fancybox-button--arrow_left" data-fancybox-prev href="javascript:;"><i class="fas fa-arrow-left"></i></a>';
$.fancybox.defaults.btnTpl.thumbs = '<a title="{{THUMBS}}" class="fancybox-button fancybox-button--thumbs" data-fancybox-thumbs href="javascript:;"><i class="fas fa-th"></i></a>';
$.fancybox.defaults.btnTpl.download = '<a title="{{DOWNLOAD}}" class="fancybox-button fancybox-button--download" data-fancybox-download href="javascript:;"><i class="fas fa-download"></i></a>';

$(function () {
    $(".photo-card a").fancybox({
        buttons: [
            "download",
            "thumbs",
            "close"
        ],
        afterShow: function(instance, current) {
            $(instance.$refs.container)
              .find("[data-fancybox-download]")
              .attr("href", current.opts.download);
        }
    });
});
