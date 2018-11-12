var stripeModule        = $('.stripe-payment-form')
var stripeModuleToken   = stripeModule.attr('data-token')
var stripeNextUrl       = stripeModule.attr('data-next-url')
var stripeBtnTitle      = stripeModule.attr('data-btn-title') || 'Add Card'
var stripeTemplate      = $.templates('#stripeTemplate')
var stripeData          = {
    pubKey: stripeModuleToken,
    nextUrl: stripeNextUrl,
    btnTitle: stripeBtnTitle
}
var stripeTemplateHTML  = stripeTemplate.render(stripeData)
stripeModule.html(stripeTemplateHTML)

/*
---------------------------------------------------------------
*/

var paymentForm = $('.payment-form')
var pubKey      = paymentForm.attr('data-token')
var nextUrl     = paymentForm.attr('data-next-url')

if (paymentForm.length == 1) {
    // Create a Stripe client.
    var stripe = Stripe(pubKey);
    // Create an instance of Elements.
    var elements = stripe.elements();
    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
      base: {
        color: '#32325d',
        lineHeight: '18px',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#aab7c4'
        }
      },
      invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
      }
    };
    // Create an instance of the card Element.
    var card = elements.create('card', {style: style});
    // Add an instance of the card Element into the `card-element` <div>.
    card.mount('#card-element');
    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function(event) {
      var displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = '';
      }
    });
    // Handle form submission.

    var form = $('#payment-form');
    var btnLoad = form.find('.btn-load')
    var btnLoadDefHtml = btnLoad.html()
    var btnLoadDefClass = btnLoad.attr('class')

    form.on('submit', function(event) {
      event.preventDefault();

      var $this = $(this)
      btnLoad.blur()
      var loadTime = 1000
      var currTimeout;
      var errorBtn = '<i class="fa fa-warning"></i> Error Occurred.'
      var errorClass = 'btn btn-danger disabled mt-2'
      var loadingBtn = '<i class="fa fa-fw fa-pulse fa-spinner"></i> Loading...'
      var loadingClass = 'btn btn-success disabled mt-2'

      stripe.createToken(card).then(function(result) {
        if (result.error) {
          // Inform the user if there was an error.
          var errorElement = $('#card-errors');
          errorElement.textContent = result.error.message;
          currTimeout = btnStatus(
            btnLoad,
            errorBtn,
            errorClass,
            1000,
            currTimeout
          )
        } else {
          // Send the token to your server.
          currTimeout = btnStatus(
            btnLoad,
            loadingBtn,
            loadingClass,
            1500,
            currTimeout
          )
          stripeTokenHandler(nextUrl, result.token);
        }
      });
    });
}

function btnStatus(element, newHtml, newClass, loadTime, timeout) {
    if (!loadTime) {
        loadTime = 1000
    }

    element.html(newHtml)
    element.removeClass(btnLoadDefClass)
    element.addClass(newClass)

    return setTimeout(function () {
        element.html(btnLoadDefHtml)
        element.removeClass(newClass)
        element.addClass(btnLoadDefClass)
    }, loadTime)
}

function redirectNext(nextPath) {
    if (nextPath) {
        setTimeout(function () {
            window.location.href = nextPath
        }, 1500)
    }
}

function stripeTokenHandler(nextUrl, token) {
    var paymentUrl = '/billing/payment/create/'
    var data = {
        'token': token.id
    }
    $.ajax({
        data: data,
        url: paymentUrl,
        method: 'POST',
        success: function (data) {
            card.clear()
            if ($.alert) {
                msg = data.message + '<i style="color:#dc3545;" class="fa fa-fw fa-pulse fa-spinner"></i> Redirecting...'
                $.alert({
                    title: '<i style="color:green; font-size:40px;" class="fa fa-smile-o"></i>',
                    content: msg,
                    theme: 'modern'
                })
            }
            btnLoad.html(btnLoadDefHtml)
            btnLoad.attr('class', btnLoadDefClass)
            redirectNext(nextUrl)
        },
        error: function (errors) {
            var msg = errors.error['message']
            $.alert({
                title: '<i style="color:red; font-size:40px;" class="fa fa-frown-o"></i><br><br> '+
                        '<i style="color:red;" class="fa fa-exclamation-triangle"></i> Oops! An error occurred.',
                content: msg,
                theme: 'modern'
            })
            btnLoad.html(btnLoadDefHtml)
            btnLoad.attr('class', btnLoadDefClass)
        }
    })
}