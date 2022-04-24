<template>
    <input id="navbar-toggler-checkbox" class="d-none" type="checkbox">
    <router-view/>
</template>

<script>
export default {
    watch:{
        $route (to, from){
            document.getElementById('navbar-toggler-checkbox').checked = false;

            if (['/user-login', '/add-user'].includes(this.$route.path)) {
                if (document.cookie.indexOf('loggedin') !== -1) {
                    // ログインしていればホームに遷移する
                    this.$router.push('/');
                }
            } else {
                if (document.cookie.indexOf('loggedin') === -1){
                    // ログインしていなければログインページに遷移する
                    this.$router.push('/user-login');
                }
            }
        }
    }
}
</script>

<style>
@import 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css';

body {
    font-size: .875rem;
    position: fixed;
    overflow: hidden;
}

.feather {
    width: 16px;
    height: 16px;
    vertical-align: text-bottom;
}

.wrapper {
    height: 100vh;
    width: 100vw;
    display: grid;
    grid-template-rows: auto minmax(0, 1fr);
    grid-template-columns: minmax(0, 1fr) minmax(0, 5fr);
}

.wrapper > header {
    grid-row: 1 / 2;
    grid-column: 1 / 3;
}

.wrapper > nav {
    grid-row: 2 / 3;
    grid-column: 1 / 2;
}

.wrapper > main {
    grid-row: 2 / 3;
    grid-column: 2 / 3;
    overflow-y: auto;
    padding: 40px 20px 60px 20px;
}

@media (max-width: 768px) {
    .wrapper {
        grid-template-columns: 0 auto;
    }

    .wrapper > nav {
        visibility: hidden;
    }

    .wrapper > main {
        padding: 40px 10px 120px 10px;
    }

    #navbar-toggler-checkbox:checked + .wrapper {
        grid-template-columns: auto 0;
    }

    #navbar-toggler-checkbox:checked + .wrapper > nav {
        visibility: visible;
    }

    #navbar-toggler-checkbox:checked + .wrapper > main {
        visibility: hidden;
    }
}

.wrapper > nav .nav-link {
    font-weight: 500;
    color: #333;
}

.wrapper > nav .nav-link.active {
    color: #2470dc;
}

.wrapper > nav .nav-link .feather {
    margin-right: 4px;
    color: #727272;
}

.wrapper > nav .nav-link.active .feather,
.wrapper > nav .nav-link:hover .feather {
    color: inherit;
}
</style>
