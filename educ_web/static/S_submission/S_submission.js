document.addEventListener('DOMContentLoaded', function() {

    // get the files uploaded with their respective file name
    let fileNames = [];
    const docUpload = document.querySelector('#upload-file');
    docUpload.addEventListener('change', function() {

        fileNames = [];

        for(let i=0; i<docUpload.files.length; i++) {
            let saveFile = docUpload.files[i].name;

            fileNames.push(saveFile);
        }

        // function to create the container of the uploaded file
        newUploadedFile(fileNames);
    });
});

// create container of recent uploaded files
function newUploadedFile(fileNames) {
    
    const submissionContainer = document.querySelector("#submission-bin-container");
    const uploadFileContainer = document.querySelector("#upload-file-container");

    fileNames.forEach(file => {
        const divContainer = document.createElement("div");
        divContainer.className = "uploaded-file-container";

        const logoDivContainer = document.createElement("div");
        logoDivContainer.className = "upload-file-logo";
        divContainer.append(logoDivContainer);

        const fileNameContainer = document.createElement("span");
        fileNameContainer.className = "file-name-context";
        fileNameContainer.innerText = file;
        
        divContainer.append(fileNameContainer);

        submissionContainer.insertBefore(divContainer, uploadFileContainer.parentNode);
    })

    uploadFileContainer.style.display = "none";
}