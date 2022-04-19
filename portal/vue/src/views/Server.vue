<template>
    <div class="wrapper">
        <Header/>
        <Sidemenu/>
        <main class="p-3 p-md-4">
            <h1 class="h3">サーバ</h1>
        </main>
    </div>
</template>

<script>
import Header from '@/components/Header.vue'
import Sidemenu from '@/components/Sidemenu.vue'

export default {
    components: {
        Header,
        Sidemenu
    }
}
</script>

<style scoped>
</style>