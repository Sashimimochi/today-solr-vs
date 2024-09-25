CREATE TABLE IF NOT EXISTS `lcc` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `media` text COLLATE utf8mb4_unicode_ci,
    `url` text COLLATE utf8mb4_unicode_ci,
    `created_at` TIMESTAMP,
    `title` text COLLATE utf8mb4_unicode_ci,
    `body` text COLLATE utf8mb4_unicode_ci,
    INDEX(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

LOAD DATA LOCAL INFILE '/data/lcc/lcc.tsv' INTO TABLE lcc FIELDS TERMINATED BY '\t' (media, `url`, `created_at`, title, body);
