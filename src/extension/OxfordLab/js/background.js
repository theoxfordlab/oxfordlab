
function init_main () {

//    chrome.cookies.get(
//        {url: 'http://127.0.0.1:8000', name:'sessionid'},
//        function(cookie){
//            if(cookie){
//                window.alert(cookie.value)
//                chrome.cookies.set(
//                    {
//                        url: 'http://127.0.0.1:8000',
//                        name: 'sessionid',
//                        value: cookie.value
//                    },
//                    function(cookie){}
//                )
//            }
//        }
//    )

    chrome.tabs.getSelected(null, function(tab) {
        url = 'http://127.0.0.1:8000/add_new_url_extension?url='+tab.url
        fetch(url, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Cache': 'no-cache'
            },
            'credentials': 'include'
        })
        .then((data) => data.json())
        .then((data) => {
            if (data["success"] == false) {
                window.alert(data["error"])
            }
        })
        .catch(error => {
                window.alert("Network error")
        })
    });
}


function getCookie(cookieName, callback){
    chrome.cookies.get(
        {
            url: 'http://127.0.0.1:8000',
            name: cookieName
        },
        function(cookie){
            if(cookie && cookie.value) {
                return callback(cookie.value, null)
            }
            return callback(null, "Error")
        }
    )
}

function setCookie(cName, cValue, callback){
    chrome.cookies.set(
        {
            url: 'http://127.0.0.1:8000',
            name: cName,
            value: cValue
        },
        function(cookie){
            if(cookie == null){
                return callback("Error in set cookies")
            }
            return callback(null)
        }
    )
}

function setCookies(callback){
    getCookie("sessionid", function(id, err){
        if(err){
            return callback("Not able to login Error in getting cookie")
        } else {
            setCookie("sessionid", id, function(err){
                if(err){
                    return callback("Not able to login Error in setting cookie")
                }
                return callback(null)
            })
        }
    })

//    chrome.cookies.get(
//        {
//            url: 'http://127.0.0.1:8000',
//            name:'sessionid'
//        },
//        function(cookie){
//            if(cookie){
//                chrome.cookies.set(
//                    {
//                        url: 'http://127.0.0.1:8000',
//                        name: 'sessionid',
//                        value: cookie.value
//                    },
//                    function(cookie){}
//                )
//            }
//        }
//    )

}




chrome.browserAction.onClicked.addListener(function(tab){
    setCookies(function(err){
        if ( err ){
            window.alert(err)
        } else {
            init_main()
            window.alert("Saved")
        }
    })
});
