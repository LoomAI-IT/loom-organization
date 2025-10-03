from internal import interface
from internal.migration.base import Migration, MigrationInfo


class AddOrganizationFieldsMigration(Migration):

    def get_info(self) -> MigrationInfo:
        return MigrationInfo(
            version="v0_0_3",
            name="add_organization_fields",
            depends_on="v0_0_1"
        )

    async def up(self, db: interface.IDB):
        queries = [
            alter_organizations_add_fields,
            alter_organizations_drop_fields
        ]

        await db.multi_query(queries)

    async def down(self, db: interface.IDB):
        queries = [
            alter_organizations_restore_fields,
            alter_organizations_drop_new_fields
        ]

        await db.multi_query(queries)

alter_organizations_drop_fields = """
ALTER TABLE organizations
    DROP COLUMN IF EXISTS autoposting_moderation;
"""

alter_organizations_add_fields = """
ALTER TABLE organizations
    ADD COLUMN IF NOT EXISTS tone_of_voice TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS brand_rules TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS compliance_rules TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS audience_insights TEXT[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS products JSONB[] DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS locale JSONB DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS additional_info TEXT[] DEFAULT '{}';
"""

alter_organizations_restore_fields = """
ALTER TABLE organizations
    ADD COLUMN IF NOT EXISTS autoposting_moderation BOOLEAN DEFAULT TRUE;
"""

alter_organizations_drop_new_fields = """
ALTER TABLE organizations
    DROP COLUMN IF EXISTS tone_of_voice,
    DROP COLUMN IF EXISTS brand_rules,
    DROP COLUMN IF EXISTS compliance_rules,
    DROP COLUMN IF EXISTS audience_insights,
    DROP COLUMN IF EXISTS products,
    DROP COLUMN IF EXISTS locale,
    DROP COLUMN IF EXISTS additional_info;
"""