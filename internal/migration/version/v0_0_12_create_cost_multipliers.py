from internal import interface
from internal.migration.base import Migration, MigrationInfo


class CreateCostMultipliersMigration(Migration):

    def get_info(self) -> MigrationInfo:
        return MigrationInfo(
            version="v0_0_12",
            name="create_cost_multipliers",
            depends_on="v0_0_3"
        )

    async def up(self, db: interface.IDB):
        await db.multi_query([create_cost_multipliers_table])

    async def down(self, db: interface.IDB):
        await db.multi_query([drop_cost_multipliers_table])

create_cost_multipliers_table = """
CREATE TABLE IF NOT EXISTS cost_multipliers (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER NOT NULL,
    generate_text_cost_multiplier REAL DEFAULT 1.0,
    generate_image_cost_multiplier REAL DEFAULT 1.0,
    generate_vizard_video_cut_cost_multiplier REAL DEFAULT 1.0,
    transcribe_audio_cost_multiplier REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
drop_cost_multipliers_table = """
DROP TABLE IF EXISTS cost_multipliers CASCADE;
"""