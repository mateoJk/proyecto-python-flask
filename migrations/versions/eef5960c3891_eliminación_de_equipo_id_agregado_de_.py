"""Eliminación de equipo_id, agregado de tipo_accesorio, modelo_dispositivo y color en la tabla Stock

Revision ID: eef5960c3891
Revises: 3eaef1be8c07
Create Date: 2024-09-12 18:49:45.530785

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eef5960c3891'
down_revision = '3eaef1be8c07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo_accesorio', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('modelo_dispositivo', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('color', sa.String(length=50), nullable=False))
        batch_op.drop_constraint('stock_ibfk_1', type_='foreignkey')
        batch_op.drop_column('equipo_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock', schema=None) as batch_op:
        batch_op.add_column(sa.Column('equipo_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('stock_ibfk_1', 'equipo', ['equipo_id'], ['id'], ondelete='CASCADE')
        batch_op.drop_column('color')
        batch_op.drop_column('modelo_dispositivo')
        batch_op.drop_column('tipo_accesorio')

    # ### end Alembic commands ###
