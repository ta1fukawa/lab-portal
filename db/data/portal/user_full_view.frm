TYPE=VIEW
query=select `portal`.`users`.`id` AS `user_id`,`portal`.`users`.`name` AS `user_name`,`portal`.`users`.`email` AS `user_email`,`portal`.`user_profile`.`birthday` AS `birthday`,`portal`.`user_profile`.`grade` AS `grade`,`portal`.`user_profile`.`position` AS `position`,`portal`.`user_profile`.`phone` AS `phone`,`portal`.`user_profile`.`address` AS `address`,`portal`.`user_profile`.`twitter` AS `twitter`,`portal`.`user_profile`.`facebook` AS `facebook`,`portal`.`user_profile`.`instagram` AS `instagram`,`portal`.`user_profile`.`linkedin` AS `linkedin`,`portal`.`user_profile`.`github` AS `github`,`portal`.`user_profile`.`website` AS `website`,`portal`.`user_profile`.`image` AS `image`,`portal`.`user_profile`.`about` AS `about`,`portal`.`user_tcu_account`.`username` AS `username`,`portal`.`tcu_account`.`mail` AS `mail`,`portal`.`tcu_account`.`usergroup` AS `usergroup`,`portal`.`tcu_account`.`name_kanji` AS `name_kanji`,`portal`.`tcu_account`.`name_kana` AS `name_kana` from (((`portal`.`users` left join `portal`.`user_profile` on(`portal`.`users`.`id` = `portal`.`user_profile`.`user_id`)) left join `portal`.`user_tcu_account` on(`portal`.`users`.`id` = `portal`.`user_tcu_account`.`user_id`)) left join `portal`.`tcu_account` on(`portal`.`user_tcu_account`.`username` = `portal`.`tcu_account`.`username`))
md5=f708d22211a7fea0de02e51001d181dc
updatable=0
algorithm=0
definer_user=root
definer_host=%
suid=2
with_check_option=0
timestamp=2022-04-19 15:17:24
create-version=2
source=SELECT
client_cs_name=utf8mb4
connection_cl_name=utf8mb4_unicode_ci
view_body_utf8=select `portal`.`users`.`id` AS `user_id`,`portal`.`users`.`name` AS `user_name`,`portal`.`users`.`email` AS `user_email`,`portal`.`user_profile`.`birthday` AS `birthday`,`portal`.`user_profile`.`grade` AS `grade`,`portal`.`user_profile`.`position` AS `position`,`portal`.`user_profile`.`phone` AS `phone`,`portal`.`user_profile`.`address` AS `address`,`portal`.`user_profile`.`twitter` AS `twitter`,`portal`.`user_profile`.`facebook` AS `facebook`,`portal`.`user_profile`.`instagram` AS `instagram`,`portal`.`user_profile`.`linkedin` AS `linkedin`,`portal`.`user_profile`.`github` AS `github`,`portal`.`user_profile`.`website` AS `website`,`portal`.`user_profile`.`image` AS `image`,`portal`.`user_profile`.`about` AS `about`,`portal`.`user_tcu_account`.`username` AS `username`,`portal`.`tcu_account`.`mail` AS `mail`,`portal`.`tcu_account`.`usergroup` AS `usergroup`,`portal`.`tcu_account`.`name_kanji` AS `name_kanji`,`portal`.`tcu_account`.`name_kana` AS `name_kana` from (((`portal`.`users` left join `portal`.`user_profile` on(`portal`.`users`.`id` = `portal`.`user_profile`.`user_id`)) left join `portal`.`user_tcu_account` on(`portal`.`users`.`id` = `portal`.`user_tcu_account`.`user_id`)) left join `portal`.`tcu_account` on(`portal`.`user_tcu_account`.`username` = `portal`.`tcu_account`.`username`))
mariadb-version=100703