"""Eliminar caracteristicas_id y agregar gama en Equipo

Revision ID: 70e6093a57f3
Revises: 4e38066bed95
Create Date: 2024-08-17 00:03:29.115201

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '70e6093a57f3'
down_revision = '4e38066bed95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('caracteristica', schema=None) as batch_op:
        batch_op.drop_constraint('caracteristica_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'modelo', ['modelo_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('equipo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gama', sa.String(length=50), nullable=True))
        batch_op.drop_constraint('equipo_ibfk_1', type_='foreignkey')
        batch_op.drop_column('caracteristicas_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('equipo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('caracteristicas_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('equipo_ibfk_1', 'caracteristica', ['caracteristicas_id'], ['id'])
        batch_op.drop_column('gama')

    with op.batch_alter_table('caracteristica', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('caracteristica_ibfk_1', 'modelo', ['modelo_id'], ['id'])

    # ### end Alembic commands ###
