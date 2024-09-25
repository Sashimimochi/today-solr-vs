CREATE TABLE IF NOT EXISTS `knbc` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `doc_id` text COLLATE utf8mb4_unicode_ci,
    `doc` text COLLATE utf8mb4_unicode_ci,
    `author` text COLLATE utf8mb4_unicode_ci,
    `emotion` text COLLATE utf8mb4_unicode_ci,
    `emotion_type` text COLLATE utf8mb4_unicode_ci,
    `emotion_object` text COLLATE utf8mb4_unicode_ci,
    INDEX(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

LOAD DATA LOCAL INFILE '/data/knbc/knbc.tsv' INTO TABLE knbc FIELDS TERMINATED BY '\t' (doc_id, doc, author, emotion, emotion_type, emotion_object);
