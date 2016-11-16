$(document).ready(function() {  
    new Dropzone(document.body, { // Make the whole body a dropzone
        url: "/api",
        previewsContainer: "#previews",
        clickable: "#clickable",
        success: function(file, response) {
            // Do nothing?
        }
    });
});