<template>
    <nav class="d-block bg-light">
        <div class="pt-3">
            <ul class="nav flex-column">
                <li class="nav-item">
                    <router-link class="nav-link" aria-current="page" to="/" active-class="active">
                    <span data-feather="home"></span>ホーム
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/tcu-portal" active-class="active">
                    <span data-feather="box"></span>大学ポータル
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/schedule" active-class="active">
                    <span data-feather="calendar"></span>スケジュール
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/server" active-class="active">
                    <span data-feather="server"></span>サーバ
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/labo-members" active-class="active">
                    <span data-feather="user"></span>研究室名簿
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link class="nav-link" to="/tcu-members" active-class="active">
                    <span data-feather="user"></span>全学名簿
                    </router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
export default {
    mounted() {
        feather.replace();
    }
}
</script>

<style>
.sidebar {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 100;
    padding: 48px 0 0;
    box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

@media (max-width: 767.98px) {
    .sidebar {
        top: 5rem;
    }
}

.sidebar-sticky {
    position: relative;
    top: 0;
    height: calc(100vh - 48px);
    padding-top: .5rem;
    overflow-x: hidden;
    overflow-y: auto;
}

.sidebar .nav-link {
    font-weight: 500;
    color: #333;
}

.sidebar .nav-link .feather {
    margin-right: 4px;
    color: #727272;
}

.sidebar .nav-link.active {
    color: #2470dc;
}

.sidebar .nav-link:hover .feather,
.sidebar .nav-link.active .feather {
    color: inherit;
}

.sidebar-heading {
    font-size: .75rem;
    text-transform: uppercase;
}
</style>