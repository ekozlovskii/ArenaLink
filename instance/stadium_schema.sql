
CREATE TABLE IF NOT EXISTS stadium (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  image_url TEXT
);

CREATE TABLE IF NOT EXISTS sector (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  stadium_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY (stadium_id) REFERENCES stadium(id)
);

CREATE TABLE IF NOT EXISTS row (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sector_id INTEGER NOT NULL,
  number INTEGER NOT NULL,
  seat_count INTEGER NOT NULL,
  FOREIGN KEY (sector_id) REFERENCES sector(id)
);

INSERT INTO stadium (id, name, image_url) VALUES (1, 'ArenaLink stadium', '/static/images/ArenaLink_stadium.jpg');


-- VIP 200
INSERT INTO sector (id, stadium_id, name) VALUES (1, 1, 'VIP 200');
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 1, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 2, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 3, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 4, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 5, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 6, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 7, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 8, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 9, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (1, 10, 29);

-- ПРЕССА 201
INSERT INTO sector (id, stadium_id, name) VALUES (2, 1, 'ПРЕССА 201');
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 1, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 2, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 3, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 4, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 5, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 6, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 7, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 8, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 9, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (2, 10, 16);

-- 202
INSERT INTO sector (id, stadium_id, name) VALUES (3, 1, '202');
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 1, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 2, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 3, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 4, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 5, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 6, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 7, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 8, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 9, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (3, 10, 18);

-- 203
INSERT INTO sector (id, stadium_id, name) VALUES (4, 1, '203');
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 1, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 2, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 3, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 4, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 5, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 6, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 7, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 8, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 9, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (4, 10, 15);

-- 204
INSERT INTO sector (id, stadium_id, name) VALUES (5, 1, '204');
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 1, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 2, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 3, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 4, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 5, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 6, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 7, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 8, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 9, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (5, 10, 21);

-- 205
INSERT INTO sector (id, stadium_id, name) VALUES (6, 1, '205');
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 1, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 2, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 3, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 4, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 5, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 6, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 7, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 8, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 9, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (6, 10, 25);

-- 206
INSERT INTO sector (id, stadium_id, name) VALUES (7, 1, '206');
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 1, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 2, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 3, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 4, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 5, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 6, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 7, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 8, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 9, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (7, 10, 29);

-- 207
INSERT INTO sector (id, stadium_id, name) VALUES (8, 1, '207');
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 1, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 2, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 3, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 4, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 5, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 6, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 7, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 8, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 9, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (8, 10, 23);

-- ПРЕМИУМ 208
INSERT INTO sector (id, stadium_id, name) VALUES (9, 1, 'ПРЕМИУМ 208');
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 1, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 2, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 3, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 4, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 5, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 6, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 7, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 8, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 9, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (9, 10, 22);

-- VIP 209
INSERT INTO sector (id, stadium_id, name) VALUES (10, 1, 'VIP 209');
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 1, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 2, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 3, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 4, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 5, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 6, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 7, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 8, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 9, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (10, 10, 10);

-- VIP 210
INSERT INTO sector (id, stadium_id, name) VALUES (11, 1, 'VIP 210');
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 1, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 2, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 3, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 4, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 5, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 6, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 7, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 8, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 9, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (11, 10, 27);

-- ПРЕМИУМ 211
INSERT INTO sector (id, stadium_id, name) VALUES (12, 1, 'ПРЕМИУМ 211');
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 1, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 2, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 3, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 4, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 5, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 6, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 7, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 8, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 9, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (12, 10, 14);

-- 212
INSERT INTO sector (id, stadium_id, name) VALUES (13, 1, '212');
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 1, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 2, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 3, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 4, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 5, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 6, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 7, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 8, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 9, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (13, 10, 14);

-- 213
INSERT INTO sector (id, stadium_id, name) VALUES (14, 1, '213');
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 1, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 2, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 3, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 4, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 5, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 6, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 7, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 8, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 9, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (14, 10, 25);

-- 214
INSERT INTO sector (id, stadium_id, name) VALUES (15, 1, '214');
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 1, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 2, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 3, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 4, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 5, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 6, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 7, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 8, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 9, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (15, 10, 10);

-- 215
INSERT INTO sector (id, stadium_id, name) VALUES (16, 1, '215');
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 1, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 2, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 3, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 4, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 5, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 6, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 7, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 8, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 9, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (16, 10, 20);

-- 216
INSERT INTO sector (id, stadium_id, name) VALUES (17, 1, '216');
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 1, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 2, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 3, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 4, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 5, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 6, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 7, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 8, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 9, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (17, 10, 28);

-- 217
INSERT INTO sector (id, stadium_id, name) VALUES (18, 1, '217');
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 1, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 2, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 3, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 4, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 5, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 6, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 7, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 8, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 9, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (18, 10, 28);

-- ПРЕМИУМ 218
INSERT INTO sector (id, stadium_id, name) VALUES (19, 1, 'ПРЕМИУМ 218');
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 1, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 2, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 3, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 4, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 5, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 6, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 7, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 8, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 9, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (19, 10, 25);

-- 501
INSERT INTO sector (id, stadium_id, name) VALUES (20, 1, '501');
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 1, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 2, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 3, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 4, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 5, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 6, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 7, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 8, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 9, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (20, 10, 13);

-- 502
INSERT INTO sector (id, stadium_id, name) VALUES (21, 1, '502');
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 1, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 2, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 3, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 4, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 5, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 6, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 7, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 8, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 9, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (21, 10, 23);

-- ЛЮКС 500
INSERT INTO sector (id, stadium_id, name) VALUES (22, 1, 'ЛЮКС 500');
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 1, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 2, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 3, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 4, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 5, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 6, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 7, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 8, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 9, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (22, 10, 13);

-- ЛЮКС 509
INSERT INTO sector (id, stadium_id, name) VALUES (23, 1, 'ЛЮКС 509');
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 1, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 2, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 3, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 4, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 5, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 6, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 7, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 8, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 9, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (23, 10, 20);

-- ЛЮКС 510
INSERT INTO sector (id, stadium_id, name) VALUES (24, 1, 'ЛЮКС 510');
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 1, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 2, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 3, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 4, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 5, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 6, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 7, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 8, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 9, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (24, 10, 17);

-- ЛЮКС 519
INSERT INTO sector (id, stadium_id, name) VALUES (25, 1, 'ЛЮКС 519');
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 1, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 2, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 3, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 4, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 5, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 6, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 7, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 8, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 9, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (25, 10, 21);

-- 503
INSERT INTO sector (id, stadium_id, name) VALUES (26, 1, '503');
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 1, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 2, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 3, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 4, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 5, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 6, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 7, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 8, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 9, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (26, 10, 23);

-- 504
INSERT INTO sector (id, stadium_id, name) VALUES (27, 1, '504');
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 1, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 2, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 3, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 4, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 5, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 6, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 7, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 8, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 9, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (27, 10, 13);

-- 505
INSERT INTO sector (id, stadium_id, name) VALUES (28, 1, '505');
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 1, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 2, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 3, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 4, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 5, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 6, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 7, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 8, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 9, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (28, 10, 15);

-- 506
INSERT INTO sector (id, stadium_id, name) VALUES (29, 1, '506');
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 1, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 2, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 3, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 4, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 5, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 6, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 7, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 8, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 9, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (29, 10, 18);

-- 507
INSERT INTO sector (id, stadium_id, name) VALUES (30, 1, '507');
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 1, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 2, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 3, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 4, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 5, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 6, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 7, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 8, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 9, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (30, 10, 10);

-- 508
INSERT INTO sector (id, stadium_id, name) VALUES (31, 1, '508');
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 1, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 2, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 3, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 4, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 5, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 6, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 7, 14);
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 8, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 9, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (31, 10, 16);

-- 511
INSERT INTO sector (id, stadium_id, name) VALUES (32, 1, '511');
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 1, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 2, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 3, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 4, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 5, 10);
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 6, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 7, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 8, 21);
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 9, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (32, 10, 25);

-- 512
INSERT INTO sector (id, stadium_id, name) VALUES (33, 1, '512');
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 1, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 2, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 3, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 4, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 5, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 6, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 7, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 8, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 9, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (33, 10, 16);

-- 513
INSERT INTO sector (id, stadium_id, name) VALUES (34, 1, '513');
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 1, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 2, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 3, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 4, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 5, 28);
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 6, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 7, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 8, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 9, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (34, 10, 27);

-- 514
INSERT INTO sector (id, stadium_id, name) VALUES (35, 1, '514');
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 1, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 2, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 3, 16);
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 4, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 5, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 6, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 7, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 8, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 9, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (35, 10, 28);

-- 515
INSERT INTO sector (id, stadium_id, name) VALUES (36, 1, '515');
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 1, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 2, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 3, 12);
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 4, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 5, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 6, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 7, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 8, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 9, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (36, 10, 30);

-- 516
INSERT INTO sector (id, stadium_id, name) VALUES (37, 1, '516');
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 1, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 2, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 3, 30);
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 4, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 5, 17);
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 6, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 7, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 8, 25);
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 9, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (37, 10, 13);

-- 517
INSERT INTO sector (id, stadium_id, name) VALUES (38, 1, '517');
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 1, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 2, 24);
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 3, 13);
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 4, 23);
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 5, 11);
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 6, 27);
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 7, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 8, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 9, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (38, 10, 27);

-- 518
INSERT INTO sector (id, stadium_id, name) VALUES (39, 1, '518');
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 1, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 2, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 3, 29);
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 4, 19);
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 5, 15);
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 6, 26);
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 7, 20);
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 8, 18);
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 9, 22);
INSERT INTO row (sector_id, number, seat_count) VALUES (39, 10, 21);