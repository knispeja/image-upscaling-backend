$(document).ready(function() {
    $("#upscaled").toggle();
    new Dropzone(document.body, { // Make the whole body a dropzone
        url: "/api",
        thumbnailWidth: null,
        thumbnailHeight: null,
        previewsContainer: "#previews",
        success: function(file, response) {
            // Hide some Dropzone elements
            $("div.dz-success-mark").remove();
            $("div.dz-error-mark").remove();
            $("div.dz-details").remove();
            $("div.dz-progress").remove();

            // Add image and make it full-size
            $("dz-image").css({"width":"100%", "height":"auto"});
            document.getElementById("upscaled").src=response;
        },
        accept: function(file, done) {
            console.log("uploaded");
            done();
        },
        init: function() {
            this.on("addedfile", function() {
                if (this.files[1]!=null){
                    this.removeFile(this.files[0]);
                } else {
                    $("#instructions").toggle();
                    $("#upscaled").toggle();
                }
            });
        }
    });
});