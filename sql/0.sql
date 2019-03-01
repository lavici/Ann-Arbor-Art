#
# IMPORTANT
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

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Art;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS ArtBid;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS TagMap;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS FavoriteArt;
DROP TABLE IF EXISTS FavoriteArtist;
DROP TABLE IF EXISTS FavoriteLocation;

SET FOREIGN_KEY_CHECKS = 1;