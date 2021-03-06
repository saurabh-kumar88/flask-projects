"""empty message

Revision ID: 716bcfd61caf
Revises: 
Create Date: 2019-03-24 12:51:09.003930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '716bcfd61caf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('BD__marg', sa.Column('specie_code', sa.Integer(), nullable=True))
    op.add_column('BK__singh__marg', sa.Column('specie_code', sa.Integer(), nullable=True))
    op.add_column('abdul__fazal__road', sa.Column('specie_code', sa.Integer(), nullable=True))
    op.add_column('akbar__road', sa.Column('specie_code', sa.Integer(), nullable=True))
    op.add_column('arch__bishop__marg', sa.Column('specie_code', sa.Integer(), nullable=True))
    op.add_column('aurangzeb__lane', sa.Column('specie_code', sa.Integer(), nullable=True))
    op.add_column('aurobindo__marg', sa.Column('specie_code', sa.Integer(), nullable=True))
    op.add_column('jashwant_singh__road', sa.Column('specie_code', sa.Integer(), nullable=True))
    op.add_column('safdarjung__road', sa.Column('specie_code', sa.Integer(), nullable=True))
    op.add_column('sardar__patel__marg', sa.Column('specie_code', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sardar__patel__marg', 'specie_code')
    op.drop_column('safdarjung__road', 'specie_code')
    op.drop_column('jashwant_singh__road', 'specie_code')
    op.drop_column('aurobindo__marg', 'specie_code')
    op.drop_column('aurangzeb__lane', 'specie_code')
    op.drop_column('arch__bishop__marg', 'specie_code')
    op.drop_column('akbar__road', 'specie_code')
    op.drop_column('abdul__fazal__road', 'specie_code')
    op.drop_column('BK__singh__marg', 'specie_code')
    op.drop_column('BD__marg', 'specie_code')
    # ### end Alembic commands ###
