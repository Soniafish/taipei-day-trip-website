// userApi_src = "http://3.18.227.207:3000/api/attraction/"+ id;
// userApi_src = "http://127.0.0.1:3000/api/attraction/"+ id;
let userApi_src = config.url + "api/user";
let user;
handel_userinfo();

//檢驗登入與否
function handel_userinfo() {
    // console.log("start handel_userinfo");

    fetch(userApi_src, { method: 'GET' }).then(function (response) {
        return response.json();//取回的字串已轉成json
    }).then(function (result) {
        // console.log(result);
        if (result == null) {
            let btn_signinToPopup = document.querySelector("#signinToPopup");
            btn_signinToPopup.classList.add("show");

            //如果是booking頁, 直接導到首頁
            if (location.href.split("/")[location.href.split("/").length - 1]=="booking"){
                document.location.href = config.url;
            }

        } else {
            user = result.data;
            let btn_signout = document.querySelector("#signout");
            btn_signout.classList.add("show");

            //如果是booking頁, 帶入username
            if (location.href.split("/")[location.href.split("/").length - 1] == "booking") {
                let userName=document.querySelector("#userName");
                userName.appendChild(document.createTextNode(result.data.name));
                document.querySelector("#order_name").value = user.name;
                document.querySelector("#order_email").value = user.email;
            }

        }

    });

}

//註冊
function regist() {
    // console.log("start regist");

    let userName = document.querySelector("#regist_username").value;
    let userEmail = document.querySelector("#regist_useremail").value;
    let userPW = document.querySelector("#regist_userpw").value;

    let error_regist_username = document.querySelector("#error_regist_username");
    let error_regist_useremail = document.querySelector("#error_regist_useremail");
    let error_regist_userpw = document.querySelector("#error_regist_userpw");
    let popup_registMessage = document.querySelector("#popup_registMessage");
    clearErrorMessage();

    if (userName == "" || userEmail == "" || userPW == "") {
        if (userName == "") {
            error_regist_username.appendChild(document.createTextNode("欄位不可為空"));
        }
        if (userEmail == "") {
            error_regist_useremail.appendChild(document.createTextNode("欄位不可為空"));
        }
        if (userPW == "") {
            error_regist_userpw.appendChild(document.createTextNode("欄位不可為空"));
        }
    }
    else {
        fetch(userApi_src, {
            method: 'POST',
            body: JSON.stringify({
                name: userName,
                email: userEmail,
                password: userPW
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function (response) {
            return response.json();
        }).then(function (result) {
            // console.log(result);
            let message="";
            if (result.hasOwnProperty('ok')) {
                message = "註冊成功, 請重新登入";
            } else {
                message = result.message;
            }
            popup_registMessage.appendChild(document.createTextNode(message));
        });

    }
}

//登入
function signin() {
    // console.log("start signin");

    let userEmail = document.querySelector("#login_useremail").value;
    let userPW = document.querySelector("#login_userpw").value;

    let error_login_useremail=document.querySelector("#error_login_useremail");
    // if (error_login_useremail.textContent!==""){
    //     error_login_useremail.removeChild(error_login_useremail.firstChild);
    // }
    let error_login_userpw=document.querySelector("#error_login_userpw");
    // if (error_login_userpw.textContent !== "") {
    //     error_login_userpw.removeChild(error_login_userpw.firstChild);
    // }
    let popup_loginMessage = document.querySelector("#popup_loginMessage");
    // if (popup_loginMessage.textContent !== "") {
    //     popup_loginMessage.removeChild(popup_loginMessage.firstChild);
    // }
    clearErrorMessage();

    if (userEmail == "" || userPW == "") {
        if (userEmail == ""){
            error_login_useremail.appendChild(document.createTextNode("欄位不可為空"));
        }
        if (userPW == "") {
            error_login_userpw.appendChild(document.createTextNode("欄位不可為空"));
        }
    }
    else{
        fetch(userApi_src, {
            method: 'PATCH',
            body: JSON.stringify({
                email: userEmail,
                password: userPW
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function (response) {
            return response.json();
        }).then(function (result) {
            // console.log(result);
            if (result.hasOwnProperty('ok')){
                location.reload();
            }else{
                popup_loginMessage.appendChild(document.createTextNode(result.message));
            }
        });
    }
    
}

//登出
function signout() {
    // console.log("start signin");
    user={};
    fetch(userApi_src, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (response) {
        return response.json();//取回的字串已轉成json
    }).then(function (result) {
        // console.log(result);
        document.location.href = config.url;
    });

}

function openPopup(id) {
    // console.log(id);
    if (document.body.classList.contains("open_popup")) {
        for (let i = 0; i < document.getElementsByClassName("popup").length; i++) {
            document.getElementsByClassName("popup")[i].classList.remove("show");
        }
    } else {
        document.body.classList.add("open_popup");
    }
    document.getElementById(id).classList.add("show");

}

function closePopup(e) {
    clearErrorMessage();

    if (e.classList.contains("pagecover")) {
        for (let i = 0; i < document.getElementsByClassName("popup").length; i++) {
            document.getElementsByClassName("popup")[i].classList.remove("show");
        }
    } else {
        e.parentElement.classList.remove("show");
    }
    document.body.classList.remove("open_popup");
}

function clearErrorMessage() {
    // console.log("clearErrorMessage");
    //註冊
    let error_regist_username = document.querySelector("#error_regist_username");
    if (error_regist_username.textContent !== "") {
        error_regist_username.removeChild(error_regist_username.firstChild);
    }
    let error_regist_useremail = document.querySelector("#error_regist_useremail");
    if (error_regist_useremail.textContent !== "") {
        error_regist_useremail.removeChild(error_regist_useremail.firstChild);
    }
    let error_regist_userpw = document.querySelector("#error_regist_userpw");
    if (error_regist_userpw.textContent !== "") {
        error_regist_userpw.removeChild(error_regist_userpw.firstChild);
    }
    let popup_registMessage = document.querySelector("#popup_registMessage");
    if (popup_registMessage.textContent !== "") {
        popup_registMessage.removeChild(popup_registMessage.firstChild);
    }

    //登入
    let error_login_useremail = document.querySelector("#error_login_useremail");
    if (error_login_useremail.textContent !== "") {
        error_login_useremail.removeChild(error_login_useremail.firstChild);
    }
    let error_login_userpw = document.querySelector("#error_login_userpw");
    if (error_login_userpw.textContent !== "") {
        error_login_userpw.removeChild(error_login_userpw.firstChild);
    }
    let popup_loginMessage = document.querySelector("#popup_loginMessage");
    if (popup_loginMessage.textContent !== "") {
        popup_loginMessage.removeChild(popup_loginMessage.firstChild);
    }

}