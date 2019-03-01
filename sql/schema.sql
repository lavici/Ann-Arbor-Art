#
# IMPORTANT
#
# If you are copying this schema into your MySQL server, make sure you drop the
# tables first. The code for that is at the top of this file or in 0.sql
#
# Also, convert indentation into spaces to avoid errors in your MySQL server.
#
# Please ensure you have MySQL configured to UTC, like so:
#
# [mysqld]
# default_time_zone='+00:00'
#
# You may also want to adjust the max packet size upwards if you're
# testing with MAMP, like so:
# max_allowed_packet = 64M
#
#
# TODO: Tombstone info: Title, Artist, Nationality, Creation Date, Life Dates, Medium


SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Art;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Image;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS ArtBid;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS TagMap;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS FavoriteArt;
DROP TABLE IF EXISTS FavoriteArtist;
DROP TABLE IF EXISTS FavoriteLocation;

SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE User(
    userID          INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username        VARCHAR(128) NOT NULL UNIQUE,
    firstName       VARCHAR(64) NOT NULL,
    lastName        VARCHAR(64) NOT NULL,
    phone           VARCHAR(64) NOT NULL,
    accountType     TINYINT NOT NULL DEFAULT 0 # 0: General user; 1: Curator; 2: Admin
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE Artist(
    artistID        INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(64) NOT NULL,
    preferredName   VARCHAR(64),
    hometown        VARCHAR(64),
    nationality     VARCHAR(64),
    yearOfBirth     INT,
    yearOfDeath     INT,
    bio             TEXT,
    image           VARCHAR(64)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE Location(
    locationID      INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(128) NOT NULL,
    address1        VARCHAR(128),   
    address2        VARCHAR(128),   
    city            VARCHAR(64),
    state           VARCHAR(64),
    zipcode         VARCHAR(16),
    type            TINYINT, # (0: museum, 1: gallery, 2: store, 3: park, 4: other)
    description     TEXT,
    latitude        FLOAT,
    longitude       FLOAT,
    image           VARCHAR(64),
    googlePlaceID   VARCHAR(128)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE Art(
    artID           INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    artistID        INT NOT NULL,
    title           TEXT NOT NULL,
    mainImage       VARCHAR(64),       
    description     TEXT,
    type            VARCHAR(64),
    height          FLOAT,
    width           FLOAT,
    depth           FLOAT,
    medium          VARCHAR(128),
    year            INT,
    locationID      INT NOT NULL,
    forSale         TINYINT DEFAULT 0, # 0; no, 1: yes
    FOREIGN KEY (artistID) REFERENCES Artist(artistID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (locationID) REFERENCES Location(locationID) ON DELETE CASCADE ON UPDATE CASCADE 
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE Image(
    imageID         INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    format          VARCHAR(4) NOT NULL,
    artID           INT NOT NULL,
    FOREIGN KEY (artID) REFERENCES Art(artID) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE Bid(
    bidID               INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    artID               INT NOT NULL,
    userID              INT NOT NULL,
    amount              INT NOT NULL,
    validBid            TINYINT NOT NULL, # 0: Not Valid; 1: Valid 
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (artID) REFERENCES Art(artID) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Make sure the increment is handled correctly. Rounded to two decimals when considering 
# constant values, and to four decimals when considering percentages.
CREATE TABLE ArtBid(
    artBidID            INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    artID               INT NOT NULL,
    startingAmount      FLOAT,
    directSale          TINYINT, # 0: no, 1: yes
    sold                TINYINT DEFAULT 0, # 0: no, 1: yes
    highestBidID        INT,
    highestBidAmount    INT, # TODO: Ask about decimal vs integer bids.
    deadline            DATETIME,
    increment           FLOAT,
    incrementType       TINYINT, # 0: percentage, 1: constant
    FOREIGN KEY (highestBidID) REFERENCES Bid(bidID),
    FOREIGN KEY (artID) REFERENCES Art(artID) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Available tag words
CREATE TABLE Tags(
    tagID       INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    tagName     VARCHAR(64) NOT NULL UNIQUE
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE TagMap(
    tagID       INT NOT NULL,
    artID       INT NOT NULL,
    PRIMARY KEY (tagID, artID),
    FOREIGN KEY (tagID) REFERENCES Tags(tagID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (artID) REFERENCES Art(artID) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# TODO: Add a paymentType (TINYINT vs VARCHAR), transaction reference 
#       (paypal payment ID - look at their API).
CREATE TABLE Transactions(
    transactionID   INT NOT NULL,
    userID          INT NOT NULL,
    artID           INT NOT NULL,
    bidID           INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (artID) REFERENCES Art(artID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (bidID) REFERENCES Bid(bidID) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE FavoriteArt(
    userID          INT NOT NULL,
    artID           INT NOT NULL,
    PRIMARY KEY (userID, artID),
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (artID) REFERENCES Art(artID)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE FavoriteArtist(
    userID          INT NOT NULL,
    artistID        INT NOT NULL,
    PRIMARY KEY (userID, artistID),
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (artistID) REFERENCES Artist(artistID)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE FavoriteLocation(
    userID          INT NOT NULL,
    locationID      INT NOT NULL,
    PRIMARY KEY (userID, locationID),
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (locationID) REFERENCES Location(locationID)
) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# ADD FULLTEXT INDEX Art and Artist
ALTER TABLE Art ADD FULLTEXT(title);
ALTER TABLE Artist ADD FULLTEXT(name);
ALTER TABLE Artist ADD FULLTEXT(preferredName);
