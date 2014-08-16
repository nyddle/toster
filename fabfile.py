#! /usr/bin/python

from fabric.api import local
import fabtools


def create_database():
    # Create DB if it does not exist
    if not fabtools.postgres.database_exists('toster'):
        fabtools.postgres.create_database('toster', owner='nyddle')


def create_user():
    # Create DB user if it does not exist
    if not fabtools.postgres.user_exists('dbuser'):
        fabtools.postgres.create_user('dbuser', password='somerandomstring')
    """
    # Create DB user with custom options
    fabtools.postgres.create_user('dbuser2', password='s3cr3t',
        createdb=True, createrole=True, connection_limit=20)
    """
