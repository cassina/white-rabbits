;(function ($){
   window.fbAsyncInit = function() {

    function login () {
      FB.login(function() {}, {scope: 'email,user_events', return_scopes: true});
    }

    function changed(response) {
      console.log('Logged in.', response);
      if (response.status === 'connected') {
        $('body').trigger('fb-login', [response]);
      } else {
        login();
      }
    }

    FB.Event.subscribe('auth.authResponseChange', changed);

    FB.init({
      appId      : '952096844837567',
      xfbml      : true,
      version    : 'v2.5',
      status: true
    });

  };

  function init() {
    (function(d, s, id){
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) {return;}
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    })(document, 'script', 'facebook-jssdk');
  }

  $(init);

})(jQuery);