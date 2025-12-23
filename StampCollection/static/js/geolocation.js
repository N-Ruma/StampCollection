const get_current_position = () => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
    } else {
        alert("Geolcation APIが搭載されていないブラウザです.")
    }
};

const successCallback = (position) => {
    const crd = position.coords;

    const latitude = crd.latitude;
    const longitude = crd.longitude;
    const accuracy = crd.accuracy;

    let element_latitude = document.getElementById("current_latitude");
    let element_longitude = document.getElementById("current_longitude");

    element_latitude.value = latitude;
    element_longitude.value = longitude;

    console.log(`latitude: ${latitude}, longitude: ${longitude}`);
};

const errorCallback = (error) => {
    switch (error.code) {
        case 1:
            alert("位置情報の利用が許可されていません.");
            break;
        case 2:
            alert("デバイスの位置を判定できません.");
            break;
        case 3:
            alert("タイムアウトが発生しました.")
            break;
        default:
            alert("位置情報を取得できません.")
            break;
    }
};