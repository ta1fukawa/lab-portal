<template>
    <div class="wrapper">
        <Header/>
        <Sidemenu/>
        <main>
            <h1 class="h3">ユーザメニュー</h1>
            <p>設定とかログアウトとか。</p>

            <h2 class="h4 mt-5">ログアウト</h2>
            <p>
                ログアウトボタンは用意していますが、他人のPCでログインしているとき以外にわざわざログアウトをする必要はないと思います。<br>
            </p>
            <button class="btn btn-primary m-2" id="logout-button">ログアウト</button>
            
            <h2 class="h4 mt-5">TCUアカウントと連携</h2>
            <p>
                下の「TCUアカウントとの連携を解除（超非推奨）」ボタンが押せたら既に連携済みだと思ってください。
            </p>
            <p>
                これを設定すると、きっといいことが起こります。
                （というか設定しないと大変なことが起こります。）
            </p>
            <p>
                他のアカウントで既に連携済みのTCUアカウントとは連携できません。<br>
                というか、同じ人が2つのアカウントを作るのは禁止しているので、当然と言えば当然の措置です。<br>
                必ず今ログインしているユーザに対応したTCUアカウントを設定してください。
            </p>
            <div class="form-group my-3">
                <label for="username">TCUアカウント</label>
                <input type="text" class="form-control" id="username" name="username" placeholder="TCUアカウント">
            </div>
            <div class="form-group my-3">
                <label for="password">パスワード</label>
                <input type="password" class="form-control" id="password" name="password" placeholder="パスワード">
            </div>
            <button class="btn btn-primary m-2" id="set-tcu-button">TCUアカウントと連携</button>
            <button class="btn btn-secondary m-2" id="remove-tcu-button">TCUアカウントとの連携を解除（超非推奨）</button>
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
    mounted() {
        var logout_button = document.getElementById('logout-button');
        logout_button.onclick = function() {
            axios_instance.post('logout')
            .then(function(response) {
                if (response.data.success) {
                    document.cookie = 'loggedin=; max-age=0';
                    window.location.reload();
                } else {
                    alert('ログアウトに失敗しました。\n' + response.data.message);
                }
            }).catch(function(error) {
                alert('ログアウトに失敗しました。');
            });
        }
        
        var set_tcu_account_button = document.getElementById('set-tcu-button');
        var remove_tcu_account_button = document.getElementById('remove-tcu-button');

        axios_instance.get('get-tcu-account')
        .then(response => {
            if (response.data.success) {
                document.getElementById('username').value = response.data.data.username;
                document.getElementById('password').value = response.data.data.password;
                set_tcu_account_button.disabled = false;
                remove_tcu_account_button.disabled = false;
            } else {
                document.getElementById('username').value = '';
                document.getElementById('password').value = '';
                set_tcu_account_button.disabled = true;
                remove_tcu_account_button.disabled = true;
            }
        })

        set_tcu_account_button.onclick = function() {
            axios_instance.post('set-tcu-account', {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            }).then(function(response) {
                if (response.data.success) {
                    alert('TCUアカウントと連携しました。');
                    remove_tcu_account_button.disabled = false;
                } else {
                    alert('TCUアカウントとの連携に失敗しました。\n' + response.data.message);
                }
            }).catch(function(error) {
                alert('TCUアカウントとの連携に失敗しました。');
            });
        }

        var username = document.getElementById('username');
        var password = document.getElementById('password');
        username.onkeydown = password.onkeydown = function(e) {
            if (username.value && password.value) {
                set_tcu_account_button.disabled = false;
            } else {
                set_tcu_account_button.disabled = true;
            }
            if (e.key === 'Enter') {
                set_tcu_account_button.click();
            }
        }

        var remove_tcu_account_button = document.getElementById('remove-tcu-button');
        remove_tcu_account_button.onclick = function() {
            axios_instance.post('remove-tcu-account')
            .then(function(response) {
                if (response.data.success) {
                    alert('TCUアカウントとの連携を解除しました。');
                    remove_tcu_account_button.disabled = true;
                } else {
                    alert('TCUアカウントとの連携を解除に失敗しました。\n' + response.data.message);
                }
            }).catch(function(error) {
                alert('TCUアカウントとの連携を解除に失敗しました。');
            });
        }
    }
}
</script>

<style scoped>
</style>