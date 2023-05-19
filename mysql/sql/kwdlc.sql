CREATE TABLE IF NOT EXISTS `kwdlc` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `body` text COLLATE utf8mb4_unicode_ci,
    INDEX(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

LOAD DATA LOCAL INFILE '/data/kwdlc/kwdlc.tsv' INTO TABLE kwdlc FIELDS TERMINATED BY '\t' (body);
