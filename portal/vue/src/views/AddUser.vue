<template>
    <div class="wrapper">
        <Header/>
        <main class="p-3 p-md-4">
            <div class="login-area">
                <h1 class="h3">ユーザ登録</h1>
                <p>
                    意外と大切なことが書いてあるので、あなたのためにも読み飛ばさないほうがいいと思います。
                </p>
                <p>
                    同じユーザが2つのアカウントを作るのは厳禁です。<br>
                    バグりはしませんが、嫌なことが起こります。
                </p>
                <p>
                    ちなみに、普通にユーザ登録をするだけでは、多くの機能が封印されています。<br>
                    封印を解くためには、どこかにいるサイトの管理者を見つけ出して【開封の儀】を行う必要があります。<br>
                    なお開封の儀の前に解呪を行いますが、研究室の関係者以外は解呪ができないため、魔を解き放たないためにも関係者以外は開封の儀をお受けしかねます。
                </p>
                <p>
                    それから、ログイン後に「ユーザーメニュー」からTCUアカウントと連携しておくことをおすすめしてます。<br>
                    というか現状、連携しないとログインできなくなる恐怖の仕様となっています。絶対に連携しましょう。
                </p>

                <div class="form-group my-3">
                    <label for="name">適当なユーザ名（今のところ、あとから変更できる機能はない。自分の名前でも入れておけ）</label>
                    <input type="text" class="form-control" id="name" name="name" placeholder="ユーザ名">
                </div>
                <div class="form-group my-3">
                    <label for="email">TCUメール以外のメールアドレス（間違えたら大変なことになるかも）</label>
                    <input type="text" class="form-control" id="email" name="email" placeholder="メールアドレス">
                </div>
                <button class="btn btn-primary m-2" id="register-button">登録して、ついでにログイン</button>
            </div>
        </main>
    </div>
</template>

<script>
import Header from '@/components/Header.vue'

export default {
    components: {
        Header
    },
    mounted() {
        var register_button = document.getElementById('register-button');
        register_button.onclick = function() {
            axios_instance.post('add-user', {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value
            }).then(function(response) {
                if (response.data.success) {
                    document.cookie = 'loggedin=yes; max-age=31536000';
                    window.location.reload();
                } else {
                    alert('登録に失敗しました。\n' + response.data.message);
                }
            }).catch(function(error) {
                alert('登録に失敗しました。');
            });
        }
        
        var username = document.getElementById('name');
        var password = document.getElementById('email');
        username.onkeydown = password.onkeydown = function(e) {
            if (e.key === 'Enter') {
                register_button.click();
            }
        }
    }
}
</script>

<style scoped>
.wrapper {
    grid-template-columns: 0 auto;
}
.login-area {
    max-width: 640px;
    margin: 0 auto;
}
</style>