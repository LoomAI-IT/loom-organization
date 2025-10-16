create_organizations_table = """
CREATE TABLE IF NOT EXISTS organizations (
    id SERIAL PRIMARY KEY,

    name TEXT NOT NULL,
    rub_balance TEXT DEFAULT '0',

    tone_of_voice TEXT[] DEFAULT '{}',
    compliance_rules JSONB[] DEFAULT '{}',
    products JSONB[] DEFAULT '{}',
    locale JSONB DEFAULT '{}',
    additional_info JSONB[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
drop_organizations_table = """
DROP TABLE IF EXISTS organizations CASCADE;
"""

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

create_organization_tables_queries = [
    create_organizations_table,
    create_cost_multipliers_table
]

drop_queries = [
    drop_cost_multipliers_table,
    drop_organizations_table
]