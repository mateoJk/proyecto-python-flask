"""Eliminar columna gama de la tabla Equipo

Revision ID: b973247b4d56
Revises: ca17873cb355
Create Date: 2024-09-09 12:09:43.919397

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b973247b4d56'
down_revision = 'ca17873cb355'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('accesorio', schema=None) as batch_op:
        batch_op.alter_column('tipo',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=50),
               nullable=True)
        batch_op.drop_constraint('accesorio_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('accesorio_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'modelo', ['modelo_id'], ['id'])
        batch_op.create_foreign_key(None, 'proveedor', ['proveedor_id'], ['id'])

    with op.batch_alter_table('equipo', schema=None) as batch_op:
        batch_op.drop_column('gama')

    with op.batch_alter_table('proveedor', schema=None) as batch_op:
        batch_op.alter_column('contacto',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('proveedor', schema=None) as batch_op:
        batch_op.alter_column('contacto',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)

    with op.batch_alter_table('equipo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gama', mysql.VARCHAR(length=50), nullable=True))

    with op.batch_alter_table('accesorio', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('accesorio_ibfk_2', 'proveedor', ['proveedor_id'], ['id'], ondelete='SET NULL')
        batch_op.create_foreign_key('accesorio_ibfk_1', 'modelo', ['modelo_id'], ['id'], ondelete='SET NULL')
        batch_op.alter_column('tipo',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###
