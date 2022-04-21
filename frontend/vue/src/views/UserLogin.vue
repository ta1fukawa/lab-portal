<template>
    <div class="wrapper">
        <Header/>
        <main>
            <div class="login-area">
                <h1 class="h3">ログイン画面</h1>
                <p>
                    ログイン画面。ここにはサイドメニューは表示されないのでとっても安心？<br>
                    ここではTCUアカウントでログインすることができます。<br>
                    現在はTCU側のパスワード更新の反映に対応していないので、新しいパスワードでログインできないときは、古いパスワードでも試してみてください。
                </p>
                <div class="form-group my-3">
                    <label for="username">TCUアカウント</label>
                    <input type="text" class="form-control" id="username" name="username" placeholder="TCUアカウント">
                </div>
                <div class="form-group my-3">
                    <label for="password">パスワード</label>
                    <input type="password" class="form-control" id="password" name="password" placeholder="パスワード">
                </div>
                <button class="btn btn-primary m-2" id="login-button">ログイン</button>

                <h2 class="h4 mt-5">ログインできないとき</h2>
                <p>
                    開発者版のサイトでは、正しい情報を入力してもログイン出来ないことがあります。（特にAPIサーバ起動直後）<br>
                    バグの可能性があるときは、諦めましょう。<br>
                    （デバッグコンソールにはAccess-Control-Allow-Originのエラーメッセージが表示されるはずです。）<br>
                    ログイン出来ないときは時間をおいたり、開き直してみたり、根気強く頑張ってみたりすることで63.212%の確率で解決できます。
                </p>
                <p>
                    まだユーザ登録をしていないときは<router-link to="/add-user">ここをクリック！</router-link>して登録してね。<br>
                    同じユーザが2つのアカウントを作るのは禁止なので、既に登録済みの人は頑張ってパスワードを思い出してログインしてください。<br>
                    悪いのはパスワード再設定ができないこのサイトではなくて、パスワードを忘れたあなた。そういうことになってます。
                </p>

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
        var login_button = document.getElementById('login-button');
        login_button.onclick = function() {
            axios_instance.post('login', {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            }).then(function(response) {
                if (response.data.success) {
                    document.cookie = 'loggedin=yes; max-age=31536000';
                    window.location.reload();
                } else {
                    alert('ログインに失敗しました。\n' + response.data.message);
                }
            }).catch(function(error) {
                alert('ログインに失敗しました。');
            });
        }
        
        var username = document.getElementById('username');
        var password = document.getElementById('password');
        username.onkeydown = password.onkeydown = function(e) {
            if (e.key === 'Enter') {
                login_button.click();
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