CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users
(
    username text PRIMARY KEY,
    pw_hash bytea NOT NULL,
    is_admin boolean DEFAULT false NOT NULL,
    is_mod boolean DEFAULT false NOT NULL,
    post_count integer DEFAULT 0,
    bio text
);

CREATE TABLE topics
(
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    title text,
    descript text
);

CREATE TABLE posts
(
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    title text,
    body text,
    author text REFERENCES users(username) ON DELETE CASCADE,
    topic_id uuid REFERENCES topics(id) ON DELETE CASCADE,
    date_ timestamp with time zone DEFAULT now()
);

CREATE TABLE replies
(
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    body text,
    author text REFERENCES users(username) ON DELETE CASCADE,
    post_id uuid REFERENCES posts(id) ON DELETE CASCADE,
    date_ timestamp with time zone DEFAULT now()
);
