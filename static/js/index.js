;(function ($) {

        window.fbAsyncInit = function() {
            FB.init({
                appId      : '952096844837567',
                xfbml      : true,
                version    : 'v2.5'
            });

            FB.getLoginStatus(function(response) {
                console.log("login status: ", response)
                if (response.status === 'connected') {
                    console.log('Logged in.');
                    loggedIn(response.authResponse);
                }
                else {
                    FB.login();
                }
            });
        };

        (function(d, s, id){
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) {return;}
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));

       var userAuth;

       function loggedIn(authResponse) {
         userAuth = authResponse;
         var avatar = 'https://graph.facebook.com/'+authResponse.userID+'/picture';
         $('input[name="fb_url"]').prop('disabled', false);
         $('input[name="fb_user_id"]').val(authResponse.userID);
         $('input[name="fb_user_token"]').val(authResponse.accessToken);
         $('#avatar').attr('src', avatar);
       }

       function disable() {
         $('form,[type="submit"]').prop('disabled', true);
         $('input[name="fb_url"]').prop('disabled', true);
       }

       function enable() {
         $('form,[type="submit"]').prop('disabled', false);
         $('input[name="fb_url"]').prop('disabled', false);
       }

       function fbUrlChanged() {
         var url = $('input[name="fb_url"]').val();
         var eventMatch = url.match(/events\/(\d+)/);

         if (!userAuth || !eventMatch) {
           $('form,[type="submit"]').prop('disabled', true);
           return;
         }
         
         var eventID = eventMatch[1];

         FB.api('/'+eventID, function (eventResponse) {
           if (eventResponse.error) {
             console.log("eventResponse ERROR", eventResponse);
           } else {
             $('#event_name').text(eventResponse.name);
             $('input[name="event_name"]').val(eventResponse.name);
             $('input[name="fb_event_id"]').val(eventResponse.id);
             $('input[name="event_time"]').val(eventResponse.start_time);
             enable();
           }
         })
       }

       function init () {
         disable();
         $('input[name="fb_url"]').on('change blur', fbUrlChanged);
       }

       $(init);
       
})(jQuery);
