// Function to check element is exist ========================================================
$.fn.exist = function(){ return $(this).length > 0; }

// Function to set color & style =============================================================
function set_color() {
  var color = localStorage.getItem('mimity-color');
  var style = localStorage.getItem('mimity-style');
  $('#color-chooser').val(color);
  $('#style-chooser').val(style);
  $('#theme').attr('href','css/style.'+color+'.'+style+'.css');
  //$('.logo img').attr('src','images/logo-'+color+'.png');
}

// Function to get current scroll position ===================================================
function get_current_scroll() {
  return document.scrollTop||document.documentElement.scrollTop||document.body.scrollTop;
}

// Wrap IIFE around the code
(function($, viewport){

  $(function(){

    // Change Color Style ======================================================================
    $('.chooser-toggle').click(function(){
      $('.chooser').toggleClass('chooser-hide');
    });
    if (localStorage.getItem('mimity-color') == null) {
      localStorage.setItem('mimity-color', 'teal');
    }
    if (localStorage.getItem('mimity-style') == null) {
      localStorage.setItem('mimity-style', 'flat');
    }
    set_color();
    $('#color-chooser').change(function(){
      localStorage.setItem('mimity-color', $(this).val());
      set_color();
    });
    $('#style-chooser').change(function(){
      localStorage.setItem('mimity-style', $(this).val());
      set_color();
    });

    // Sticky Middle Header ====================================================================
    var lastScrollTop = 0;
    $(window).scroll(function(){

      var cs = get_current_scroll();
      if (cs > lastScrollTop) {
        // scroll down
        var limiter = 170
      } else {
        // scroll up
        var limiter = 64
      }
      lastScrollTop = cs;

      var top_header        = $('.top-header');
      var middle_header     = $('.middle-header');
      var middle_header_row = $('.middle-header .row');
      var logo_img          = $('.logo img');
      var logo_h4           = $('.logo h4');
      var logo_a            = $('.logo a');
      var search_box        = $('.search-box');
      var cart_btn          = $('.cart-btn');

      logo_h4.remove();
      if (cs > limiter) {
        if (viewport.is('<=sm')) {
          top_header.addClass('mt-139');
          middle_header_row.addClass('pb-10');
          logo_img.addClass('hide');
          logo_a.append('<h4>'+logo_img.data('text-logo')+'</h4>');
          search_box.add(cart_btn).removeClass('m-t-2');
        } else {
          top_header.addClass('mt-94');
        }
        middle_header.addClass('sticky');
      } else {
        top_header.removeClass('mt-94');
        top_header.removeClass('mt-139');
        middle_header_row.removeClass('pb-10');
        logo_img.removeClass('hide');
        middle_header.removeClass('sticky');
        search_box.add(cart_btn).addClass('m-t-2');
      }
    });

    // open dropdown on hover for desktop only =================================================
    $('ul.nav li.dropdown').hover(function() {
      if (viewport.is('>xs')) {
        $(this).addClass('open');
      }
    }, function() {
      if (viewport.is('>xs')) {
        $(this).removeClass('open');
      }
    });

    // Navigation submenu ======================================================================
    $('ul.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
      event.preventDefault();
      event.stopPropagation();
      $(this).parent().siblings().removeClass('open');
      $(this).parent().toggleClass('open');
    });

    // owlCarousel for Home Slider =============================================================
    if ($('.home-slider').exist()) {
      $('.home-slider').owlCarousel({
        items:1,
        loop:true,
        autoplay:true,
        autoplayHoverPause:true,
        dots:false,
        nav:true,
        navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
      });
    }

    // owlCarousel for Widget Slider ===========================================================
    if ($('.widget-slider').exist()) {
      var widget_slider = $('.widget-slider');
      widget_slider.owlCarousel({
        items:1,
        dots: false,
        nav: true,
        navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
        responsive:{
          0:{
            items:2,
          },
          768:{
            items:3,
          },
          992:{
            items:1,
          }
        }
      });
    }

    // owlCarousel for Product Slider ==========================================================
    if ($('.product-slider').exist()) {
      var product_slider = $('.product-slider')
      product_slider.owlCarousel({
        dots: false,
        nav: true,
        navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
        responsive:{
            0:{
              items:2,
            },
            768:{
              items:3,
            },
            1200:{
              items:4,
            }
          }
      });
    }

     // owlCarousel for Related Product Slider =================================================
    if ($('.related-product-slider').exist()) {
      var related_product_slider = $('.related-product-slider')
      related_product_slider.owlCarousel({
        dots: false,
        nav: true,
        navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
        responsive:{
            0:{
              items:2,
            },
            768:{
              items:3,
            },
            992:{
              items:5,
            },
            1200:{
              items:6,
            }
          }
      });
    }

    // owlCarousel for Brand Slider ============================================================
    if ($('.brand-slider').exist()) {
      var brand_slider = $('.brand-slider');
      brand_slider.owlCarousel({
        dots:false,
        nav:true,
        navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
        responsive:{
          0:{
            items:2,
            margin:10
          },
          480:{
            items:2,
            margin:15
          },
          768:{
            items:3,
            margin:15
          },
          992:{
            items:4,
            margin: 30
          },
          1200:{
            items:6,
            margin: 30
          }
        }
      });
    }

    // Tooltip =================================================================================
    $('button[data-toggle="tooltip"]').tooltip({container:'body',animation:false});
    $('a[data-toggle="tooltip"]').tooltip({container:'body',animation:false});

    // Back top Top ============================================================================
      $(window).scroll(function(){
      if ($(this).scrollTop()>70) {
        $('.back-top').fadeIn();
      } else {
        $('.back-top').fadeOut();
      }
    });

    // Touchspin ===============================================================================
    if ($('.input-qty').exist()) {
      $('.input-qty input').TouchSpin({
        verticalbuttons: true,
        prefix: 'qty'
      });
    }

    // Typeahead example =======================================================================

    $('.search-input').typeahead({
      fitToElement: true,
      source: search,
    });

    function search(query,process) {
      console.log('-|->',query)
      $.ajax({
        type:"GET",
        url: "/s/shop/",
        data:{
          'q':query,
        },
        success:process,
        dataType:'json'
      });
    }
    /*
    $('.search-input').keyup(function() {
      $.ajax({
        type:"GET",
        url: "/api/search/shop/",
        data:{
          'q':$('.search-input').val(),
        },
        success:searchSuccess,
        dataType:'json'
      });
    });

    function searchSuccess (data,textStatus, jqXHR){
      $('.search-input').typeahead({
        fitToElement: true,
        source: [{"name":"Poly Bag","language":"en","instance":"product","url":"http://localhost:8000/demo-store/Bags/Poly-Bag","link_to":{"url":"shop.product","shop":"demo-store","product":"Poly-Bag","category":"Bags"},"image":"https://res.cloudinary.com/ftrina/image/upload/v1474206116/igangrf8ai6tfomwfdtf.jpg","verified":true,"verified_person":true,"verified_business":true,"followers":10,"rating":{"count":0,"average":0.0,"total":0,"percentage":0.0},"country":"EG","orders":10,"id":"5e1e5c15-da08-48d1-9509-35f221817693"}],
        autoSelect: true
    });
      console.log(data)

    }
*/


/*

    function searchSuccess (data,textStatus, jqXHR){
      console.log('-->',data)
    }

*/


    // metisMenu for vertical-menu =============================================================
    if ($('.vertical-menu').exist()) {
      $('.vertical-menu').metisMenu();
    }

    // Function to set owl cover height via data-*breakpoint*-height ===========================
    function set_owl_cover_height() {
      $('.owl-cover').each(function(){
        $(this).css('background-image', 'url(' + decodeURIComponent($(this).data('src')) + ')');
        if (viewport.is('>=xs')) {
          if ($(this).attr('data-xs-height')) {
            $(this).css('height', $(this).data('xs-height'));
          }
        }
        if (viewport.is('>=sm')) {
          if ($(this).attr('data-sm-height')) {
            $(this).css('height', $(this).data('sm-height'));
          }
        }
        if (viewport.is('>=md')) {
          if ($(this).attr('data-md-height')) {
            $(this).css('height', $(this).data('md-height'));
          }
        }
        if (viewport.is('>=lg')) {
          if ($(this).attr('data-lg-height')) {
            $(this).css('height', $(this).data('lg-height'));
          }
        }
      });
    }

    // set owl cover height ====================================================================
    if ($('.owl-cover').exist()) {
      set_owl_cover_height();
      $(window).resize(function(){
        set_owl_cover_height();
      });
    }

  });

})(jQuery, ResponsiveBootstrapToolkit);