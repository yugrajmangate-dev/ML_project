from alembic.config import Config
from alembic import command
import os

def upgrade():
    cfg = Config('alembic.ini')
    command.upgrade(cfg, 'head')

def downgrade():
    cfg = Config('alembic.ini')
    command.downgrade(cfg, 'base')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['upgrade', 'downgrade'], help='Migration action')
    args = parser.parse_args()
    if args.action == 'upgrade':
        upgrade()
    else:
        downgrade()
