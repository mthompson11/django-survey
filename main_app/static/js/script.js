const imageToggle = document.getElementById('image-toggle');

imageToggle.addEventListener('click', function(){
    const imageLabelEl = document.getElementById('edit-image-label');
    const imageInputEl = document.getElementById('image-edit-input');
    if(imageInputEl){
        imageLabelEl.remove();
        imageInputEl.remove();
        imageToggle.textContent = 'New Photo'
    }else{
        const imageLabelEl = document.createElement('label')
        imageLabelEl.setAttribute('for', 'image_input');
        imageLabelEl.setAttribute('id', 'edit-image-label');
        imageLabelEl.classList.add('form-label')
        imageLabelEl.textContent = 'Image'
        const inputEl = document.createElement('input')
        inputEl.type = 'file'
        inputEl.name = 'photo-file'
        inputEl.classList.add('form-control')
        inputEl.setAttribute('id', 'image-edit-input')
        const surveyFormEl = document.getElementById('survey-edit-form-body');
        surveyFormEl.appendChild(imageLabelEl);
        surveyFormEl.appendChild(inputEl);
        imageToggle.textContent = 'Keep Old Photo'
    }
});