let bookingApi_src = config.url + "api/booking";

//前往預定行程頁
function getBooking() {
    let signinToPopup = document.querySelector("#signinToPopup");
    if (signinToPopup.classList == "btn_txt show"){
        openPopup('popup_login');
    }else{
        document.location.href = config.url +"booking";
    }
}

//建立預定行程
function setBooking() {
    let signinToPopup = document.querySelector("#signinToPopup");
    //尚未登入
    if (signinToPopup.classList == "btn_txt show") {
        openPopup('popup_login');
        return;
    } 

    //已登入
    let attration_trip_id = location_href[location_href.length - 1];
    let attration_trip_date = document.querySelector("#attration_trip_date").value;
    let attration_trip_time = document.querySelector("input[name='time']:checked").value;
    let attration_trip_cost = document.querySelector("#attration_trip_cost").textContent;

    let booking = {
        "attractionId": attration_trip_id,
        "date": attration_trip_date,
        "time": attration_trip_time,
        "price": attration_trip_cost
    }
    console.log(booking);
    fetch(bookingApi_src, {
        method: 'POST',
        body: JSON.stringify(booking),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (response) {
        return response.json();
    }).then(function (result) {
        // console.log(result);
        if (result.hasOwnProperty('ok')) {
            document.location.href = config.url + "booking";
        } else {
            alert(result.message);
        }
        
    });

}