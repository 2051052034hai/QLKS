
const get_day_of_time = (d1, d2) => {
    let ms1 = d1.getTime();
    let ms2 = d2.getTime();
    return Math.ceil((ms2 - ms1) / (24*60*60*1000));
};

function addtocart(id, tenPhong, donGia){
    event.preventDefault()

    var ngayNhan = document.getElementById("ngayNhan").value
    var ngayTra = document.getElementById("ngayTra").value
    var soLuong = Number(document.getElementById("soluong").value)
    var day_nhan = new Date(ngayNhan)
    var day_tra = new Date(ngayTra)
    var soNgayThue = get_day_of_time(day_nhan, day_tra)
    var loaiKhach = Number(document.getElementById("select").value)
    var day_check = 28
    var today = new Date()
    var check_28_day = get_day_of_time(today, day_nhan)

    if(ngayNhan == '' || ngayTra == '')
        return confirm("Ngày nhận và trả phòng không được để trống !!");

    if (check_28_day <= 0 )
        return confirm("Ngày nhận không được nhỏ hơn ngày hiện tại !!");

    if (check_28_day > day_check){
        return confirm("Ngày nhận phòng không được quá 28 ngày so với hiện tại!!");
    }

    if(soNgayThue <= 0)
    {
        return confirm("Bạn cần nhập số ngày nhận lớn hơn ngày trả!!");
    }


    fetch('/api/add-cart',{
    method:'post',
    body: JSON.stringify({
        'id':id,
        'tenPhong':tenPhong,
        'donGia':donGia,
        'ngayNhanPhong':ngayNhan,
        'ngayTraPhong': ngayTra,
        'soNgayThue':soNgayThue,
        'soLuongKhach': soLuong,
        'loaiKhach':loaiKhach,

    }),
    headers:{
            'Content-Type': 'application/json'
    }
    }).then(function(res){

        return res.json()
    }).then(function(data){
        let imgElement = document.getElementById("img")
        let hrefElement = imgElement.getAttribute("src");

        console.info(data)

        let gio = document.getElementById("gio")
        gio.classList.add('style_class');
        let all_cart = document.getElementById("all")
        all_cart.innerHTML =` <div class="all_cart">
                      <div class="media">
                        <a class="thumbnail pull-left" href="#"> <img class="media-object" src="${hrefElement}" style="width: 40px; height: 40px;"> </a>
                        <h5>${data.tenPhong}</h5>
                      </div>
                      <div class="content-cart">
                        <td class="col-sm-1 col-md-1 text-center"><strong>Ngày nhận phòng: </strong>${data.ngayNhanPhong}</td>
                        <td class="col-sm-1 col-md-1 text-center"><strong>Ngày trả phòng:</strong>${data.ngayTraPhong}</td>
                        <td class="col-sm-1 col-md-1 text-center"><strong>Số Ngày Thuê:</strong>${data.soNgayThue}</td>
                        <td class="col-sm-1 col-md-1 text-center"><strong>Giá Thuê:</strong>${data.tienThue} VNĐ</td>
                        <button type="button" class="btn btn-danger" style="font-size: 10px">Xoá</button>
                      </div>
                    </div> `

    }).catch(function(err){
        console.error(err)
    })
}

function pay(){
    if (confirm('Bạn có chắc muốn thanh toán hay không ?') == true){


         console.log("ngfwwafaf")
        fetch('/api/pay',{
            method:'post'
            }).then(res => res.json()).then( data => {

                 console.log(data);

                if (data.code == 200)
                    location.reload()

            }).catch(err => console.error(err))
            }
    }