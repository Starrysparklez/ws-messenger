--- KEY --------------- TYPE -------------- DEFAULTS ---
CREATE TABLE IF NOT EXISTS users(
    id                  VARCHAR             PRIMARY KEY NOT NULL,
    username            VARCHAR(24)         NOT NULL,
    role                VARCHAR             DEFAULT NULL,
    password_hash       VARCHAR(120)        NOT NULL,
    created_at          TIMESTAMP           DEFAULT CURRENT_TIMESTAMP,
    locale_code         VARCHAR(5)          DEFAULT 'en_US',
    discriminator       VARCHAR(4)          DEFAULT '0000'
);
CREATE TABLE IF NOT EXISTS channels(
    id                  VARCHAR             PRIMARY KEY NOT NULL,
    name                VARCHAR(24)         NOT NULL,
    topic               VARCHAR(128)        DEFAULT NULL,
    created_at          TIMESTAMP           DEFAULT CURRENT_TIMESTAMP,
    type                VARCHAR(8)          NOT NULL
);
CREATE TABLE IF NOT EXISTS messages(
    id                  VARCHAR             PRIMARY KEY NOT NULL,
    channel_id          VARCHAR             NOT NULL,
    author_id           VARCHAR             NOT NULL,
    content             VARCHAR(2000)       NOT NULL,
    created_at          TIMESTAMP           DEFAULT CURRENT_TIMESTAMP
);
