<template>
    <div class="wrapper">
        <Header/>
        <Sidemenu/>
        <main>
            <h1 class="h3">研究室名簿</h1>

            <div v-for="(group, key) in members" :key="key">
                <h2 class="h4 mt-3">{{key}}</h2>
                <div class="card-group">
                    <div v-for="(person, key) in group" :key="key" class="card m-3 d-flex flex-row" style="max-width: 440px;align-items: flex-start;">
                        <img v-if="person.image" class="img-fluid rounded-start flex-grow-1" :src="require(`@/assets/members/${person.image}`)">
                        <img v-else class="img-fluid rounded-start" :src="require(`@/assets/members/dummy.png`)">
                        <div class="card-body">
                            <div>
                                <h5 class="card-title d-inline-block">{{person.name_kanji}}</h5><span v-if="person.position" class="ms-2 text-muted">{{person.position}}</span>
                            </div>
                            <p v-if="person.about" class="card-text">{{person.about}}</p>
                            <div class="card-text small">
                                <div v-if="person.phone"><a :href="'tel:' + person.phone" class="text-muted"><span class="me-1" data-feather="phone"></span>{{person.phone}}</a></div>
                                <div v-if="person.user_email"><a :href="'mailto:' + person.user_email" class="text-muted"><span class="me-1" data-feather="mail"></span>{{person.user_email}}</a></div>
                                <div v-if="person.twitter"><a :href="'https://twitter.com/' + person.twitter" class="text-muted" target="_blank" rel="noopener noreferrer"><span class="me-1" data-feather="twitter"></span>{{person.twitter}}</a></div>
                                <div v-if="person.facebook"><a :href="'https://www.facebook.com/' + person.facebook" class="text-muted" target="_blank" rel="noopener noreferrer"><span class="me-1" data-feather="facebook"></span>{{person.facebook}}</a></div>
                                <div v-if="person.linkedin"><a :href="'https://jp.linkedin.com/in/' + person.linkedin" class="text-muted" target="_blank" rel="noopener noreferrer"><span class="me-1" data-feather="linkedin"></span>{{person.linkedin}}</a></div>
                                <div v-if="person.github"><a :href="'https://github.com/' + person.github" class="text-muted" target="_blank" rel="noopener noreferrer"><span class="me-1" data-feather="github"></span>{{person.github}}</a></div>
                                <div v-if="person.website"><a :href="person.website" class="text-muted"><span class="me-1" data-feather="link"></span>Website</a></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

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
    },
    data() {
        return {
            members: {}
        }
    },
    mounted() {
        axios_instance.get('lab-members').then(response => {
            if (response.data.success) {
                this.members = response.data.data.members;
            } else {
                alert('研究室名簿の取得に失敗しました。\n' + response.data.message);
            }
        });
    },
    updated() {
        feather.replace();
    }
}
</script>

<style scoped>
.sub-wrapper {
    display: grid;
    height: calc(100vh - 160px);
    grid-template-columns: 1fr 3fr;
}

.sub-left {
    grid-column: 1 / 2;
    overflow-y: auto;
}

.sub-right {
    grid-column: 2 / 3;
    overflow-y: auto;
}
</style>