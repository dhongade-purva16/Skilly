"""Add phase 2 foundation tables

Revision ID: b4f812345678
Revises: 395207f68399
Create Date: 2026-09-24 12:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'b4f812345678'
down_revision: Union[str, Sequence[str], None] = '395207f68399'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. target_companies
    op.create_table('target_companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('normalized_name', sa.String(), nullable=True),
        sa.Column('website', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True, default=True),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_target_companies_id'), 'target_companies', ['id'], unique=False)
    op.create_index(op.f('ix_target_companies_name'), 'target_companies', ['name'], unique=False)
    op.create_index(op.f('ix_target_companies_normalized_name'), 'target_companies', ['normalized_name'], unique=True)

    # 2. target_company_roles
    op.create_table('target_company_roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.Column('career_role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['career_role_id'], ['career_roles.id'], ),
        sa.ForeignKeyConstraint(['company_id'], ['target_companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_target_company_roles_id'), 'target_company_roles', ['id'], unique=False)

    # 3. target_company_role_skills
    op.create_table('target_company_role_skills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('target_company_role_id', sa.Integer(), nullable=True),
        sa.Column('skill_id', sa.Integer(), nullable=True),
        sa.Column('required_proficiency_level', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ),
        sa.ForeignKeyConstraint(['target_company_role_id'], ['target_company_roles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_target_company_role_skills_id'), 'target_company_role_skills', ['id'], unique=False)

    # 4. student_career_goals add column target_company_id
    op.add_column('student_career_goals', sa.Column('target_company_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_student_career_goals_target_company', 'student_career_goals', 'target_companies', ['target_company_id'], ['id'])

    # 5. student_professional_profiles
    op.create_table('student_professional_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('headline', sa.String(), nullable=True),
        sa.Column('current_status', sa.String(), nullable=True),
        sa.Column('experience_level', sa.String(), nullable=True),
        sa.Column('years_of_experience', sa.Float(), nullable=True),
        sa.Column('professional_summary', sa.String(), nullable=True),
        sa.Column('work_domain', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id')
    )
    op.create_index(op.f('ix_student_professional_profiles_id'), 'student_professional_profiles', ['id'], unique=False)

    # 6. student_external_profiles
    op.create_table('student_external_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('github_url', sa.String(), nullable=True),
        sa.Column('linkedin_url', sa.String(), nullable=True),
        sa.Column('portfolio_url', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('student_id')
    )
    op.create_index(op.f('ix_student_external_profiles_id'), 'student_external_profiles', ['id'], unique=False)

    # 7. student_resumes
    op.create_table('student_resumes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('content_type', sa.String(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('extracted_text', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_resumes_id'), 'student_resumes', ['id'], unique=False)
    op.create_index(op.f('ix_student_resumes_student_id'), 'student_resumes', ['student_id'], unique=False)

    # 8. student_evidence
    op.create_table('student_evidence',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('source_url', sa.String(), nullable=True),
        sa.Column('evidence_type', sa.String(), nullable=False),
        sa.Column('extracted_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_synced_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('verification_status', sa.String(), nullable=True, default='unverified'),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_evidence_id'), 'student_evidence', ['id'], unique=False)

    # 9. assessments add column target_company_id
    op.add_column('assessments', sa.Column('target_company_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_assessments_target_company', 'assessments', 'target_companies', ['target_company_id'], ['id'])

def downgrade() -> None:
    op.drop_constraint('fk_assessments_target_company', 'assessments', type_='foreignkey')
    op.drop_column('assessments', 'target_company_id')
    op.drop_index(op.f('ix_student_evidence_id'), table_name='student_evidence')
    op.drop_table('student_evidence')
    op.drop_index(op.f('ix_student_resumes_student_id'), table_name='student_resumes')
    op.drop_index(op.f('ix_student_resumes_id'), table_name='student_resumes')
    op.drop_table('student_resumes')
    op.drop_index(op.f('ix_student_external_profiles_id'), table_name='student_external_profiles')
    op.drop_table('student_external_profiles')
    op.drop_index(op.f('ix_student_professional_profiles_id'), table_name='student_professional_profiles')
    op.drop_table('student_professional_profiles')
    op.drop_constraint('fk_student_career_goals_target_company', 'student_career_goals', type_='foreignkey')
    op.drop_column('student_career_goals', 'target_company_id')
    op.drop_index(op.f('ix_target_company_role_skills_id'), table_name='target_company_role_skills')
    op.drop_table('target_company_role_skills')
    op.drop_index(op.f('ix_target_company_roles_id'), table_name='target_company_roles')
    op.drop_table('target_company_roles')
    op.drop_index(op.f('ix_target_companies_normalized_name'), table_name='target_companies')
    op.drop_index(op.f('ix_target_companies_name'), table_name='target_companies')
    op.drop_index(op.f('ix_target_companies_id'), table_name='target_companies')
    op.drop_table('target_companies')
