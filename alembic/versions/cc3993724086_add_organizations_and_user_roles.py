"""add organizations and user roles

Revision ID: cc3993724086
Revises: b0cedde34d33
Create Date: 2026-01-07 22:21:33.208801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc3993724086'
down_revision: Union[str, Sequence[str], None] = 'b0cedde34d33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    user_role = sa.Enum('OWNER', 'BARBER', 'ADMIN', name='userrole')
    user_role.create(op.get_bind())

    # 2. Criar a tabela organizations
    op.create_table('organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('slug', sa.String(), nullable=True),
        sa.Column('segment', sa.String(), nullable=True),
        sa.Column('plan_type', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_id'), 'organizations', ['id'], unique=False)
    op.create_index(op.f('ix_organizations_name'), 'organizations', ['name'], unique=False)
    op.create_index(op.f('ix_organizations_slug'), 'organizations', ['slug'], unique=True)


    op.add_column('users', sa.Column('organization_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('role', user_role, nullable=False, server_default='OWNER'))
    
    # 4. Criar a chave estrangeira
    op.create_foreign_key(None, 'users', 'organizations', ['organization_id'], ['id'])


def downgrade():
    # Ordem inversa para desfazer
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role')
    op.drop_column('users', 'organization_id')
    
    op.drop_index(op.f('ix_organizations_slug'), table_name='organizations')
    op.drop_index(op.f('ix_organizations_name'), table_name='organizations')
    op.drop_index(op.f('ix_organizations_id'), table_name='organizations')
    op.drop_table('organizations')
    
    # Destruir o tipo Enum por último
    user_role = sa.Enum('OWNER', 'BARBER', 'ADMIN', name='userrole')
    user_role.drop(op.get_bind())