create_organizations_table = """
CREATE TABLE IF NOT EXISTS organizations (
    id SERIAL PRIMARY KEY,
    
    name TEXT NOT NULL,
    rub_balance NUMERIC(15,2) DEFAULT 0.00,
    autoposting_moderation BOOLEAN DEFAULT TRUE,
    publication_text_end_sample TEXT DEFAULT '',
    video_cut_description_end_sample TEXT DEFAULT '',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
drop_organizations_table = """
DROP TABLE IF EXISTS organizations CASCADE;
"""

create_organization_tables_queries = [
    create_organizations_table
]

drop_organization_tables_queries = [
    drop_organizations_table
]