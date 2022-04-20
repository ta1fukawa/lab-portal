CREATE TABLE IF NOT EXISTS `users` (
    `id`         int          NOT NULL AUTO_INCREMENT,
    `name`       varchar(255) NOT NULL,
    `email`      varchar(255) NOT NULL,
    `created_at` datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `removed_at` datetime,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user_profile` (
    `user_id`    int NOT NULL,
    `birthday`   date,
    `grade`      varchar(255),
    `position`   varchar(255),
    `phone`      varchar(255),
    `address`    varchar(255),
    `twitter`    varchar(255),
    `facebook`   varchar(255),
    `instagram`  varchar(255),
    `linkedin`   varchar(255),
    `github`     varchar(255),
    `website`    varchar(255),
    `image`      varchar(255),
    `about`      text,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tcu_account` (
    `username`      varchar(255) NOT NULL,
    `hash_password` varchar(255) NOT NULL,
    `mail`          varchar(255) NOT NULL,
    `usergroup`     varchar(255) NOT NULL,
    `name_kanji`    varchar(255) NOT NULL,
    `name_kana`     varchar(255) NOT NULL,
    `created_at`    datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`    datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user_tcu_account` (
    `user_id`      int          NOT NULL,
    `username`     varchar(255) NOT NULL,
    `password`     varchar(255) NOT NULL,
    `created_at`   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`username`) REFERENCES `tcu_account` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `roles` (
    `id`         int          NOT NULL AUTO_INCREMENT,
    `name`       varchar(255) NOT NULL,
    `created_at` datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user_role` (
    `user_id`    int      NOT NULL,
    `role_id`    int      NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`, `role_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE VIEW IF NOT EXISTS `user_full_view` AS
SELECT
    `users`.`id`    AS `user_id`,
    `users`.`name`  AS `user_name`,
    `users`.`email` AS `user_email`,
    `user_profile`.`birthday`  AS `birthday`,
    `user_profile`.`grade`     AS `grade`,
    `user_profile`.`position`  AS `position`,
    `user_profile`.`phone`     AS `phone`,
    `user_profile`.`address`   AS `address`,
    `user_profile`.`twitter`   AS `twitter`,
    `user_profile`.`facebook`  AS `facebook`,
    `user_profile`.`instagram` AS `instagram`,
    `user_profile`.`linkedin`  AS `linkedin`,
    `user_profile`.`github`    AS `github`,
    `user_profile`.`website`   AS `website`,
    `user_profile`.`image`     AS `image`,
    `user_profile`.`about`     AS `about`,
    `user_tcu_account`.`username`   AS `username`,
    `tcu_account`.`mail`       AS `mail`,
    `tcu_account`.`usergroup`  AS `usergroup`,
    `tcu_account`.`name_kanji` AS `name_kanji`,
    `tcu_account`.`name_kana`  AS `name_kana`
FROM `users`
    LEFT JOIN `user_profile` ON `users`.`id` = `user_profile`.`user_id`
    LEFT JOIN `user_tcu_account` ON `users`.`id` = `user_tcu_account`.`user_id`
    LEFT JOIN `tcu_account` ON `user_tcu_account`.`username` = `tcu_account`.`username`;

CREATE TABLE IF NOT EXISTS `tcu_portal_message` (
    `id`           int          NOT NULL,
    `user_id`      int          NOT NULL,
    `date`         datetime     NOT NULL,
    `sender`       varchar(255) NOT NULL,
    `title`        varchar(255) NOT NULL,
    `is_important` tinyint(1)   NOT NULL DEFAULT 0,
    `body`         text         NOT NULL,
    `created_at`   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tcu_portal_oshirase` (
    `id`           int          NOT NULL,
    `user_id`      int          NOT NULL,
    `date`         date         NOT NULL,
    `registrant`   varchar(255) NOT NULL,
    `title`        varchar(255) NOT NULL,
    `body`         text         NOT NULL,
    `created_at`   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tcu_portal_daredemo` (
    `id`           int          NOT NULL,
    `user_id`      int          NOT NULL,
    `date`         date         NOT NULL,
    `registrant`   varchar(255) NOT NULL,
    `title`        varchar(255) NOT NULL,
    `body`         text         NOT NULL,
    `created_at`   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at`   datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
