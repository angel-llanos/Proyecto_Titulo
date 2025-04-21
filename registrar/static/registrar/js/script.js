document.addEventListener("DOMContentLoaded", function () {

    const registerTab = document.querySelector('#register-tab');
    const registerPane = document.querySelector('#register');
    
    if (registerPane && registerPane.querySelector('.errorlist')) {
        const tabTrigger = new bootstrap.Tab(registerTab);
        tabTrigger.show();
    }
});