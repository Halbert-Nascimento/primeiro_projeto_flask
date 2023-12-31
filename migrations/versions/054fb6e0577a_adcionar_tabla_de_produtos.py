"""Adcionar tabla de produtos

Revision ID: 054fb6e0577a
Revises: 
Create Date: 2023-11-15 01:22:40.556691

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '054fb6e0577a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('produto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome_produto', sa.String(length=255), nullable=False),
    sa.Column('tipo_produto', sa.String(length=255), nullable=True),
    sa.Column('descricao_produto', sa.Text(), nullable=True),
    sa.Column('imagem1', sa.String(length=255), nullable=True),
    sa.Column('imagem2', sa.String(length=255), nullable=True),
    sa.Column('imagem3', sa.String(length=255), nullable=True),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('produtos')
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('telefone',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=20),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('telefone',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=20),
               nullable=False)

    op.create_table('produtos',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nome_produto', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('tipo_produto', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('descricao_produto', mysql.TEXT(), nullable=True),
    sa.Column('imagem1', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('imagem2', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('imagem3', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('id_usuario', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='MyISAM'
    )
    op.drop_table('produto')
    # ### end Alembic commands ###
