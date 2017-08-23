$(document).ready(function() {
    var errorHandler = function(event, id, fileName, reason) {
        qq.log("id: " + id + ", fileName: " + fileName + ", reason: " + reason);
    };

    var fileNum = 0;
    
    $('#picker').fineUploader({
        /*autoUpload: false,*/
        uploadButtonText: "Select Files",
        request: {
            endpoint: "/upload/receiver"
        },
        validation: {
            /*allowedExtensions: ['*'],*/
            sizeLimit: 5000000000
        },
        text: {
            uploadButton: "Click Or Drag & Drop file"
        },
        failedUploadTextDisplay: {
            mode: 'custom',
            maxChars: 5
        }
    }).on('error', errorHandler);

    $('#triggerUpload').click(function() {
        $('#picker').fineUploader("uploadStoredFiles");
    });
    
    
});