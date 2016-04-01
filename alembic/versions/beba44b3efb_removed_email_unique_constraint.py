revision = 'beba44b3efb'
down_revision = '32903473e4ba'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint(u'email', 'user', type_='unique')


def downgrade():
    op.create_unique_constraint(u'email', 'user', ['email'])
