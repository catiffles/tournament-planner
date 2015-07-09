#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def db_connect(sql, params=False):
    """Connect to the database, and close the connection when the action is complete"""
    con = connect()
    cursor = con.cursor()
    cursor.execute(sql, params)
    con.commit()
    con.close()


def db_con_return(sql, params=False):
    """Connect to the database, closes the connection when the action is complete, and returns the query"""
    con = connect()
    cursor = con.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    con.close()
    return result


def deleteMatches():
    """Remove all the match records from the database."""

    db_connect("DELETE FROM matches;")


def deletePlayers():
    """Remove all the player records from the database."""

    db_connect("DELETE FROM players;")


def countPlayers():
    """Returns the number of players currently registered."""

    count = db_con_return("SELECT COUNT(*) FROM players;")

    return int(count[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db_connect("INSERT INTO players VALUES (DEFAULT, %s);", (name, ))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in
    first place, or a player tied for first place if
    there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    return db_con_return("SELECT * FROM ranking ORDER BY wins DESC")


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db_connect(
        "INSERT INTO matches (winner, loser) VALUES  (%s, %s)",
        (winner, loser))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    ranking = playerStandings()
    num = len(ranking)
    pairings = []

    for player in range(0, num, 2):
        pair = ((ranking[player][0], ranking[player][1],
                ranking[player + 1][0], ranking[player + 1][1]))
        pairings.append(pair)

    return pairings
