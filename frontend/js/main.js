const API_URL = 'http://127.0.0.1:5000/';

function displayImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $("#preview").attr("src", e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function formSubmit() {
    $.ajax({
        url: API_URL,
        method: 'POST',
        processData: false,
        contentType: false,
        xhrFields: {
            withCredentials: false
        },
        crossDomain: true,
        data: new FormData($("#imageUploader")[0]),
        success: (data) => {
            alert("We did it Reddit!" + data);
        }
    });
}