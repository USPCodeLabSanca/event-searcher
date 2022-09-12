function geoip(json){
    let userip      = document.getElementById("user_ip");
    let city = document.getElementById("user_city");
    userip.textContent      = json.ip;
    city.textContent = json.city;
    alert("OI");
}