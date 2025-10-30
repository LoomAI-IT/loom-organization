from internal import interface
from internal.migration.base import Migration, MigrationInfo


class UpdateOrganizationFieldsMigration(Migration):

    def get_info(self) -> MigrationInfo:
        return MigrationInfo(
            version="v1_0_0",
            name="update_organization_fields",
            depends_on="v0_0_12"
        )

    async def up(self, db: interface.IDB):
        queries = [
            convert_compliance_rules_to_jsonb,
            convert_additional_info_to_jsonb,
            drop_unused_organization_fields,
            add_description_field
        ]

        await db.multi_query(queries)

    async def down(self, db: interface.IDB):
        queries = [
            restore_unused_organization_fields,
            convert_compliance_rules_to_text_array,
            convert_additional_info_to_text_array,
            delete_description_field
        ]

        await db.multi_query(queries)

# Migration UP queries

convert_compliance_rules_to_jsonb = """
ALTER TABLE organizations
    DROP COLUMN IF EXISTS compliance_rules,
    ADD COLUMN compliance_rules JSONB[] DEFAULT '{}';
"""

convert_additional_info_to_jsonb = """
ALTER TABLE organizations
    DROP COLUMN IF EXISTS additional_info,
    ADD COLUMN additional_info JSONB[] DEFAULT '{}';
"""

add_description_field = """
ALTER TABLE organizations
    ADD COLUMN IF NOT EXISTS description TEXT DEFAULT '';
"""

drop_unused_organization_fields = """
ALTER TABLE organizations
    DROP COLUMN IF EXISTS video_cut_description_end_sample,
    DROP COLUMN IF EXISTS publication_text_end_sample,
    DROP COLUMN IF EXISTS brand_rules,
    DROP COLUMN IF EXISTS audience_insights;
"""

# Migration DOWN queries

restore_unused_organization_fields = """
ALTER TABLE organizations
    ADD COLUMN IF NOT EXISTS video_cut_description_end_sample TEXT DEFAULT '',
    ADD COLUMN IF NOT EXISTS publication_text_end_sample TEXT DEFAULT '',
    ADD COLUMN IF NOT EXISTS brand_rules TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS audience_insights TEXT[] DEFAULT '{}';
"""

delete_description_field = """
ALTER TABLE organizations
    DROP COLUMN IF EXISTS description;
"""

convert_compliance_rules_to_text_array = """
ALTER TABLE organizations
    DROP COLUMN IF EXISTS compliance_rules,
    ADD COLUMN compliance_rules TEXT[] DEFAULT '{}';
"""

convert_additional_info_to_text_array = """
ALTER TABLE organizations
    DROP COLUMN IF EXISTS additional_info,
    ADD COLUMN additional_info TEXT[] DEFAULT '{}';
"""
