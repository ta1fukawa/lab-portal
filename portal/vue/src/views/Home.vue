<template>
    <div class="wrapper">
        <Header/>
        <Sidemenu/>
        <main class="p-3 p-md-4">
            <h1 class="h3">ホーム</h1>

            <p>
                スマホ対応しているつもりですが、そこまでテストしていないので、問題があったらごめんなさい。
            </p>
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