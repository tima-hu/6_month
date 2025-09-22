window.fbAsyncInit = function() {
  FB.init({
    appId      : '828000679762918',
    cookie     : true,
    xfbml      : true,
    version    : 'v17.0'
  });
};

(function(d, s, id){
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement(s); js.id = id;
   js.src = "https://connect.facebook.net/en_US/sdk.js";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

function checkLoginState() {
  FB.getLoginStatus(function(response) {
    if (response.status === 'connected') {
      const fbToken = response.authResponse.accessToken;

      fetch('http://localhost:8000/api/auth/facebook/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_token: fbToken })
      })
      .then(res => res.json())
      .then(data => {
        console.log('DRF token:', data.token);
      });
    } else {
      console.log('Not authenticated');
    }
  });
}
