<template>
    <div class="wrapper">
        <Header/>
        <Sidemenu/>
        <main class="p-3 p-md-4">
            <h1 class="h3">大学ポータル</h1>

            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <div class="me-2 align-items-center d-flex text-secondary">20:15更新</div>
                <button class="btn btn-secondary btn-sm" type="button">最新の情報に更新<span class="ms-1" data-feather="refresh-cw"></span></button>
            </div>
            
            <div class="my-3 p-3 bg-body rounded shadow-sm">
                <h2 class="h6 m-0 pb-2">#スター付きの投稿</h2>

                <div class="list-group list-group-flush border-top">
                    <a href="#" class="list-group-item p-2 d-flex border-bottom bg-light">
                        <div class="flex-shrink-0 rounded bg-info d-flex align-items-center justify-content-center text-white" style="width: 32px; height: 32px;">東</div>
                        <div class="flex-grow-1 overflow-hidden ms-2 text-secondary">
                            <div class="d-flex w-100 justify-content-between">
                                <div>
                                    <span class="badge bg-danger me-1">重要</span>
                                    <h5 class="my-list-header mb-0 d-inline-block">新型コロナワクチン未接種者の方へ</h5>
                                    <span class="ms-2 blockquote-footer">東京都市大学</span>
                                </div>
                                <small>2022/04/08</small>
                            </div>
                            <p class="m-0 my-list-body text-truncate">本学では安心安全に修学できるように ワクチン未接種及び 2 回目の接種後 2 週間を経過していない方は、 PCR 検査などを受けていただき、ウイルスが検出されなければ、 それが確認された日から 1 週間は登学できることとしています。 授業などの出席にはできるだけワクチンを接種することをおすすめします。</p>
                        </div>
                    </a>
                </div>
            </div>
            
            <div class="my-3 p-3 bg-body rounded shadow-sm">
                <div class="d-flex w-100 justify-content-between">
                    <h2 class="h6 m-0 pb-2">#未読の投稿</h2>
                    <a class="text-secondary" href="#">すべて既読にする</a>
                </div>

                <div class="list-group list-group-flush border-top">
                    <a href="#" class="list-group-item p-2 d-flex border-bottom">
                        <div class="flex-shrink-0 rounded bg-primary d-flex align-items-center justify-content-center text-white" style="width: 32px; height: 32px;">S</div>
                        <div class="flex-grow-1 overflow-hidden ms-2">
                            <div class="d-flex w-100 justify-content-between">
                                <div>
                                    <h5 class="my-list-header mb-0 d-inline-block">学生食堂メニュー（4/11～）のお知らせ</h5>
                                    <span class="ms-2 blockquote-footer">SC学生支援センター</span>
                                </div>
                                <small>2022/04/08</small>
                            </div>
                            <p class="m-0 my-list-body text-truncate">4/11～16の 学生食堂のおすすめメニューです。 4/13(水)～15(金)は都市大ソフトクリーム　ポイント3倍デー　となります。 この機会に是非ご賞味ください。 他にも4/1に7号館カフェがオープンし、世田谷キャンパスでは4つの飲食エリアでお食事いただけます。 なお、ラウンジオークの学生利用可能な時間帯は13：00～14：00となりますので、ご注意ください。</p>
                        </div>
                    </a>

                    <a href="#" class="list-group-item p-2 d-flex border-bottom">
                        <div class="flex-shrink-0 rounded bg-secondary d-flex align-items-center justify-content-center text-white" style="width: 32px; height: 32px;">M</div>
                        <div class="flex-grow-1 overflow-hidden ms-2">
                            <div class="d-flex w-100 justify-content-between">
                                <div>
                                    <h5 class="my-list-header mb-0 d-inline-block">（新歓）一緒にレースカーを作りませんか？？</h5>
                                    <span class="ms-2 blockquote-footer">Mi-Tech Racing（箕田　賢太郎）</span>
                                </div>
                                <small>2022/04/09</small>
                            </div>
                            <p class="m-0 my-list-body text-truncate">新入生の皆さん、ご入学おめでとうございます！！ そろそろ授業が始まり、本格的に大学生が始まった感じがしますね、、 さて、皆さん、入るサークルは決まりましたでしょうか？ 入っていないそこのあなたへ、、 Mi-Tech Racingのご紹介です！ Q:　そもそもMi-Tech Racingって何ですか？ A:　Mi-Tech Racingとは東京都市大学の学生フォーミュラチームです。 ９月に行われる学生フォーミュラ大会を目指して１年かけて１台のマシンを製作します。</p>
                        </div>
                    </a>
                </div>
            </div>
            
            <div class="my-3 p-3 bg-body rounded shadow-sm">
                <h2 class="h6 m-0 pb-2">#最近の投稿</h2>

                <div class="list-group list-group-flush border-top">
                    <a href="#" class="list-group-item p-2 d-flex border-bottom bg-light">
                        <div class="flex-shrink-0 rounded bg-info d-flex align-items-center justify-content-center text-white" style="width: 32px; height: 32px;">東</div>
                        <div class="flex-grow-1 overflow-hidden ms-2 text-secondary">
                            <div class="d-flex w-100 justify-content-between">
                                <div>
                                    <span class="badge bg-danger me-1">重要</span>
                                    <h5 class="my-list-header mb-0 d-inline-block">新型コロナワクチン未接種者の方へ</h5>
                                    <span class="ms-2 blockquote-footer">東京都市大学</span>
                                </div>
                                <small>2022/04/08</small>
                            </div>
                            <p class="m-0 my-list-body text-truncate">本学では安心安全に修学できるように ワクチン未接種及び 2 回目の接種後 2 週間を経過していない方は、 PCR 検査などを受けていただき、ウイルスが検出されなければ、 それが確認された日から 1 週間は登学できることとしています。 授業などの出席にはできるだけワクチンを接種することをおすすめします。</p>
                        </div>
                    </a>

                    <a href="#" class="list-group-item p-2 d-flex border-bottom bg-light">
                        <div class="flex-shrink-0 rounded bg-info d-flex align-items-center justify-content-center text-white" style="width: 32px; height: 32px;">（</div>
                        <div class="flex-grow-1 overflow-hidden ms-2 text-secondary">
                            <div class="d-flex w-100 justify-content-between">
                                <div>
                                    <h5 class="my-list-header mb-0 d-inline-block">こころの健康調査の実施について</h5>
                                    <span class="ms-2 blockquote-footer">（世田谷）教育・学生支援センター</span>
                                </div>
                                <small>2022/04/07</small>
                            </div>
                            <p class="m-0 my-list-body text-truncate">あなたの大切な時間を過ごすために こころの健康調査の入力をお願いします。 ◇東京都市大学 学生相談室 では「こころの健康調査」を行っています。 ◇大学生活をおくる上で、身体的健康とこころの健康は大切です。 ◇本学では学生のこころの健康の維持増進を推進しています。この結果は本学での健康増進を図るための基礎資料として使用します。 </p>
                        </div>
                    </a>

                    <a href="#" class="list-group-item p-2 d-flex border-bottom">
                        <div class="flex-shrink-0 rounded bg-primary d-flex align-items-center justify-content-center text-white" style="width: 32px; height: 32px;">S</div>
                        <div class="flex-grow-1 overflow-hidden ms-2">
                            <div class="d-flex w-100 justify-content-between">
                                <div>
                                    <h5 class="my-list-header mb-0 d-inline-block">学生食堂メニュー（4/11～）のお知らせ</h5>
                                    <span class="ms-2 blockquote-footer">SC学生支援センター</span>
                                </div>
                                <small>2022/04/08</small>
                            </div>
                            <p class="m-0 my-list-body text-truncate">4/11～16の 学生食堂のおすすめメニューです。 4/13(水)～15(金)は都市大ソフトクリーム　ポイント3倍デー　となります。 この機会に是非ご賞味ください。 他にも4/1に7号館カフェがオープンし、世田谷キャンパスでは4つの飲食エリアでお食事いただけます。 なお、ラウンジオークの学生利用可能な時間帯は13：00～14：00となりますので、ご注意ください。</p>
                        </div>
                    </a>

                    <a href="#" class="list-group-item p-2 d-flex border-bottom bg-light">
                        <div class="flex-shrink-0 rounded bg-primary d-flex align-items-center justify-content-center text-white" style="width: 32px; height: 32px;">S</div>
                        <div class="flex-grow-1 overflow-hidden ms-2 text-secondary">
                            <div class="d-flex w-100 justify-content-between">
                                <div>
                                    <h5 class="my-list-header mb-0 d-inline-block">4/11～　100円朝食・夕食営業　開始のお知らせ</h5>
                                    <span class="ms-2 blockquote-footer">SC学生支援センター</span>
                                </div>
                                <small>2022/04/08</small>
                            </div>
                            <p class="m-0 my-list-body text-truncate">4/11（月）より100円朝食と夕食営業を開始します。 営業時間は 100円朝食　8：30～10：00 夕食営業　15：20～19：20 場所は学生食堂（9号館）です。 詳しいメニューについては学生食堂のHPをご確認ください。 またご利用の際は 登学に係るガイドラインおよび新型コロナウイルス感染防止対策を遵守のうえ、 ご利用ください。</p>
                        </div>
                    </a>

                    <a href="#" class="list-group-item p-2 d-flex border-bottom">
                        <div class="flex-shrink-0 rounded bg-secondary d-flex align-items-center justify-content-center text-white" style="width: 32px; height: 32px;">M</div>
                        <div class="flex-grow-1 overflow-hidden ms-2">
                            <div class="d-flex w-100 justify-content-between">
                                <div>
                                    <h5 class="my-list-header mb-0 d-inline-block">（新歓）一緒にレースカーを作りませんか？？</h5>
                                    <span class="ms-2 blockquote-footer">Mi-Tech Racing（箕田　賢太郎）</span>
                                </div>
                                <small>2022/04/09</small>
                            </div>
                            <p class="m-0 my-list-body text-truncate">新入生の皆さん、ご入学おめでとうございます！！ そろそろ授業が始まり、本格的に大学生が始まった感じがしますね、、 さて、皆さん、入るサークルは決まりましたでしょうか？ 入っていないそこのあなたへ、、 Mi-Tech Racingのご紹介です！ Q:　そもそもMi-Tech Racingって何ですか？ A:　Mi-Tech Racingとは東京都市大学の学生フォーミュラチームです。 ９月に行われる学生フォーミュラ大会を目指して１年かけて１台のマシンを製作します。</p>
                        </div>
                    </a>

                    <a href="#" class="list-group-item p-2 d-flex border-bottom bg-light">
                        <div class="flex-shrink-0 rounded bg-secondary d-flex align-items-center justify-content-center text-white" style="width: 32px; height: 32px;">体</div>
                        <div class="flex-grow-1 overflow-hidden ms-2 text-secondary">
                            <div class="d-flex w-100 justify-content-between">
                                <div>
                                    <h5 class="my-list-header mb-0 d-inline-block">【新入部員募集中】サッカー経験者、初心者、マネージャー大歓迎です！！</h5>
                                    <span class="ms-2 blockquote-footer">体育会サッカー部（河野　なつみ）</span>
                                </div>
                                <small>2022/04/08</small>
                            </div>
                            <p class="m-0 my-list-body text-truncate">体育会サッカー部です！ 新入生の皆様、ご入学おめでとうございます！ サッカー部では新入部員を募集しています！ 〇基本情報〇 在籍部員数…25名（選手：23名　MG：2名） 活動日…水、土、日（リーグ期間中は毎週末試合が入ります） 練習場所…東京都市大学総合グラウンド アルバイトやボランティアなどの両立も可能です。 世田谷、横浜の両キャンパスの学生が在籍しています。 </p>
                        </div>
                    </a>
                </div>

                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                    <a class="mt-1 p-1" href="#">続きを表示<span data-feather="chevron-down"></span></a>
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
    }
}
</script>

<style scoped>
.my-list-header {
    font-size: 0.85rem;
}

.my-list-body {
    font-size: 0.85rem;
}
</style>