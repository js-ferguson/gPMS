function editProfile() {
    const element = document.querySelector('#user-profile');
    element.style.display = 'none';

    const form = document.querySelector('#user-profile-form');
    form.style.display = 'inline-block';
}

function editClinic() {
    const element = document.querySelector('#clinic-profile');
    element.style.display = 'none';

    const form = document.querySelector('#clinic-profile-form');
    form.style.display = 'inline-block';
}

function editMods() {
    const element = document.querySelector('.mod-list');
    const button = document.querySelector('#edit-modalities-button');
    element.style.display = 'none';
    button.style.display = 'none';

    const form = document.querySelector('#mod-list-form');
    form.style.display = 'inline-block';
}
