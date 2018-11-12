$(document).ready(function () {
//    contact form related
    var contactForm     = $('.contact')
    var contactMethod   = contactForm.attr('method')
    var contactUrl      = contactForm.attr('action')

    contactForm.submit(function (e) {
        e.preventDefault()
        var contactData = contactForm.serialize()
        $.ajax({
            url: contactUrl,
            method: contactMethod,
            data: contactData,
            success: function (data) {
                contactForm[0].reset()
                $.alert({
                    title: '<i style="color:green; font-size:40px;" class="fa fa-smile-o"></i>',
                    content: data.message,
                    theme: 'modern'
                })
            },
            error: function (errorlog) {
                contactForm[0].reset()
                console.log(errorlog)
                var json = errorlog.responseJSON
                var msg = ''
                $.each(json, function (key, value) {
                    msg += value[0].message + '<br>'
                })
                $.alert({
                    title: '<i style="color:red; font-size:40px;" class="fa fa-frown-o"></i><br><br> Oops!'+
                            ' An error occurred.',
                    content: msg,
                    theme: 'modern'
                })
            }
        })
    })

//    search related (auto)
    var searchForm      = $('.search-form')
    var searchInput     = searchForm.find('[name="q"]')
    var searchBtn       = searchForm.find('[type="submit"]')
    var typingInterval  = 500
    var typingTime      = 0

    searchInput.keyup(function (e) {
        clearTimeout(typingTime)
        typingTime = setTimeout(performSearch, typingInterval)
    })
    searchInput.keydown(function (e) {
        clearTimeout(typingTime)
    })
    function loader () {
        searchBtn.addClass('disabled text-white')
        searchBtn.html('<i class="fa fa-spin fa-spinner"></i>')
    }
    function performSearch () {
        loader()
        var query = searchInput.val()
        setTimeout(function () {
            window.location.href = '/search/?q=' + query
        }, 1000)
    }

//    product & cart related
    var productForm = $('.prod-update-ajax')
    productForm.submit(function (e) {
        e.preventDefault();
        var thisForm    = $(this)
        // var actionUrl = thisForm.attr('action')
        var actionUrl   = thisForm.attr('data-endpoint')
        var httpMethod  = thisForm.attr('method')
        var formData    = thisForm.serialize()

        $.ajax({
            url: actionUrl,
            method: httpMethod,
            data: formData,
            success: function (data) {
                console.log('-- success called --');
                var submitted = thisForm.find('.submit-span')
                if (data.added) {
                    submitted.html('\
                        Added to cart &nbsp; \
                        <button class="btn btn-sm text-uppercase" type="submit">\
                            <i class="fa fa-minus-circle" style="color:red"></i> Remove\
                        </button>\
                    ')
                } else {
                    submitted.html('\
                        <button class="btn btn-sm btn-warning text-uppercase" type="submit">\
                            <i class="fa fa-plus-circle" style="color:white"></i> Add to cart\
                        </button>\
                    ')
                }
                console.log(actionUrl)
                // counts cart items and setting it
                var counter = $('.cart-counter')
                counter.text(data.cartItemCount)

                var currPath = window.location.href
                if (currPath.indexOf('cart') != -1) {
                    refreshCart()
                }
            },
            error: function (errorData) {
                $.alert({
                    title: 'Oops!',
                    content: "We've encountered a problem.",
                    theme: 'modern'
                })
            }
        })
    })

    function refreshCart() {
        var cartHome            = $('.cart-home')
        var cartBody            = cartHome.find('.cart-body')
        var cartSummary         = $('.cart-summary')
        var productRows         = cartBody.find('.cart-product')
        var subtotal            = cartSummary.find('.cart-subtotal')
        var total               = cartSummary.find('.cart-total')
        var refreshCartUrl      = '/api/cart'
        var refreshMethod       = 'GET'
        var data                = {}
        var currUrl             = window.location.href

        $.ajax({
            url: refreshCartUrl,
            method: refreshMethod,
            data: data,
            success: function (data) {
                var hiddenRemove = $('.cart-item-remove')
                if (data.products.length > 0) {
                    productRows.html('')
                    i = data.products.length
                    $.each(data.products, function (index, value) {
                        console.log(value)
                        var newRemove = hiddenRemove.clone()
                        newRemove.css('display', 'block')
                        newRemove.find('.cart-item-id').val(value.id)
                        cartBody.prepend('<tr><th scope="row">'
                            + i +'</th><td><a class="text-danger text-uppercase" style="font-weight:bold" href="'
                            + value.url + '">'
                            + value.name +'</a></td><td>'
                            + value.description.trimToLength(50) +'</td><td>'
                            + value.price +'</td><td>'
                            + newRemove.html() +'</tr>'
                        )

                        i--
                    })
                    subtotal.text(data.subtotal)
                    total.text(data.total)
                } else {
                    window.location.href = currUrl
                }
            },
            error: function (errorData) {
                $.alert({
                    title: '<i style="color:red; font-size:40px;" class="fa fa-frown-o"></i><br><br>Oops!',
                    content: "We've encountered a problem.",
                    theme: 'modern'
                })
            }
        })
    }
})

// truncate characters
String.prototype.trimToLength = function(m) {
  return (this.length > m)
    ? jQuery.trim(this).substring(0, m).split(" ").slice(0, -1).join(" ") + "..."
    : this;
};
