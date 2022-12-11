const get_day_of_time = (d1, d2) => {
    let ms1 = d1.getTime();
    let ms2 = d2.getTime();
    return Math.ceil((ms2 - ms1) / (24*60*60*1000));
};

function addtocart(id, tenPhong, donGia){

    var ngayNhan = document.getElementById("ngayNhan").value
    var ngayTra = document.getElementById("ngayTra").value
    var soLuong = document.getElementById("soluong").value

    var day_nhan = new Date(ngayNhan)
    var day_tra = new Date(ngayTra)
    var soNgayThue = get_day_of_time(day_nhan, day_tra)

    fetch('/api/add-cart',{
    method:'post',
    body: JSON.stringify({
        'id':id,
        'tenPhong':tenPhong,
        'donGia':donGia,
        'ngayNhanPhong':ngayNhan,
        'ngayTraPhong': ngayTra,
        'soNgayThue':soNgayThue
    }),
    headers:{
            'Content-Type': 'application/json'
    }
    }).then(function(res){
        console.info(res)
        return res.json()
    }).then(function(data){
         console.info(data)

        let all_cart = document.getElementById("all")
        console.log(all_cart)
        all_cart.innerHTML = "<h1> ngyen thanh hai </h1>"
    }).catch(function(err){
        console.error(err)
    })
}