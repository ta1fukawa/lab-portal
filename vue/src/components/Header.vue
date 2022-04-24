<template>
    <header class="navbar navbar-dark bg-dark flex-wrap flex-md-nowrap p-0 shadow">
        <router-link class="navbar-brand col-md-3 col-lg-2 me-0 px-3" to="/">神野研ポータル</router-link>
        <button class="navbar-toggler position-absolute d-md-none collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation">
            <label for="navbar-toggler-checkbox"><span class="navbar-toggler-icon"></span></label>
        </button>
        <input class="form-control form-control-dark w-100 d-md-block d-none" type="text" placeholder="検索（未実装です！）" aria-label="Search" disabled>
        <div class="w-md-0 w-100"></div>
        <div class="navbar-nav" id="user-menu">
            <div class="nav-item text-nowrap">
                <router-link class="nav-link px-3" to="/user-menu" active-class="active">ユーザメニュー</router-link>
            </div>
        </div>
    </header>
</template>

<style>
.navbar-brand {
    padding-top: .75rem;
    padding-bottom: .75rem;
    font-size: 1rem;
    background-color: rgba(0, 0, 0, .25);
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .25);
}

.navbar .navbar-toggler {
    top: .25rem;
    right: 1rem;
}

.navbar .form-control {
    padding: .75rem 1rem;
    border-width: 0;
    border-radius: 0;
}

.form-control-dark, .form-control-dark:disabled {
    color: #fff;
    background-color: rgba(255, 255, 255, .1);
    border-color: rgba(255, 255, 255, .1);
}

.form-control-dark:focus {
    border-color: transparent;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, .25);
}

@media (min-width: 768px) {
    .w-md-0 {
        display: none;
    }
}

@media (max-width: 767.98px) {
    #navbar-toggler-checkbox + .wrapper > header > #user-menu {
        display: none;
    }

    #navbar-toggler-checkbox:checked + .wrapper > header > #user-menu {
        display: block;
        line-height: 2.5;
    }
}
</style>