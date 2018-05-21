/*!
 * bootstrap-fileinput v4.4.9
 * http://plugins.krajee.com/file-input
 *
 * Font Awesome icon theme configuration for bootstrap-fileinput. Requires font awesome assets to be loaded.
 *
 * Author: Kartik Visweswaran
 * Copyright: 2014 - 2018, Kartik Visweswaran, Krajee.com
 *
 * Licensed under the BSD 3-Clause
 * https://github.com/kartik-v/bootstrap-fileinput/blob/master/LICENSE.md
 */
(function ($) {
    "use strict";

    $.fn.fileinputThemes.fa = {
        
        fileActionSettings: {
            removeIcon: '<i class="fa fa-trash"></i>',
            uploadIcon: '<i class="fa fa-upload"></i>',
            uploadRetryIcon: '<i class="fa fa-repeat"></i>',
            downloadIcon: '<i class="fa fa-download"></i>',
            zoomIcon: '<i class="fa fa-search-plus"></i>',
            dragIcon: '<i class="fa fa-arrows"></i>',

            indicatorNew: '<i class="fa fa-plus-circle text-warning"></i>',
            indicatorSuccess: '<i class="fa fa-check-circle text-success"></i>',
            indicatorError: '<i class="fa fa-exclamation-circle text-danger"></i>',
            indicatorLoading: '<i class="fa fa-hourglass text-muted"></i>',




        removeIcon: '<i class="batch-icon batch-icon-bin-alt-2"></i>',
        removeClass: 'btn-ftrina',
        removeErrorClass: 'btn btn-sm btn-kv btn-danger',
        removeTitle: 'Remove file',

        uploadIcon: '<i class="batch-icon  batch-icon-browser-upload"></i>',
        uploadClass: 'btn-ftrina',
        uploadTitle: 'Upload file',
        uploadRetryIcon: '<i class="glyphicon glyphicon-repeat"></i>',

        uploadRetryTitle: 'Retry upload',

        downloadIcon: '<i class="glyphicon glyphicon-download"></i>',
        downloadClass: 'btn-ftrina',
        downloadTitle: 'Download file',

        zoomIcon: '<i class="batch-icon batch-icon-zoom-in-alt"></i>',
        zoomClass: 'btn-ftrina',
        zoomTitle: 'View Details',



        },
        layoutTemplates: {
            fileIcon: '<i class="fa fa-file kv-caption-icon"></i> '
        },
        previewZoomButtonIcons: {
            prev: '<i class="fa fa-caret-left fa-lg"></i>',
            next: '<i class="fa fa-caret-right fa-lg"></i>',
            toggleheader: '<i class="fa fa-fw fa-arrows-v"></i>',
            fullscreen: '<i class="fa fa-fw fa-arrows-alt"></i>',
            borderless: '<i class="fa fa-fw fa-external-link"></i>',
            close: '<i class="fa fa-fw fa-remove"></i>'
        },
        previewFileIcon: '<i class="fa fa-file"></i>',
        browseIcon: '<i class="fa fa-folder-open"></i>',
        removeIcon: '<i class="fa fa-trash"></i>',
        cancelIcon: '<i class="fa fa-ban"></i>',
        uploadIcon: '<i class="fa fa-upload"></i>',
        msgValidationErrorIcon: '<i class="fa fa-exclamation-circle"></i> '
    };
})(window.jQuery);

