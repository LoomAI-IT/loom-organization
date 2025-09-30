from internal import interface, model
from internal.migration.base import Migration, MigrationInfo


class InitialSchemaMigration(Migration):

    def get_info(self) -> MigrationInfo:
        return MigrationInfo(
            version="v0_0_1",
            name="initial_schema",
        )

    async def up(self, db: interface.IDB):
        queries = [
            create_organizations_table
        ]

        await db.multi_query(queries)

    async def down(self, db: interface.IDB):
        queries = [
            drop_organizations_table
        ]

        await db.multi_query(queries)

create_organizations_table = """
CREATE TABLE IF NOT EXISTS organizations (
    id SERIAL PRIMARY KEY,
    
    name TEXT NOT NULL,
    rub_balance TEXT DEFAULT '0',
    autoposting_moderation BOOLEAN DEFAULT TRUE,
    publication_text_end_sample TEXT DEFAULT '',
    video_cut_description_end_sample TEXT DEFAULT '',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
drop_organizations_table = """
DROP TABLE IF EXISTS organizations CASCADE;
"""