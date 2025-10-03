create_organizations_table = """
CREATE TABLE IF NOT EXISTS organizations (
    id SERIAL PRIMARY KEY,
    
    name TEXT NOT NULL,
    rub_balance TEXT DEFAULT '0',
    video_cut_description_end_sample TEXT DEFAULT '',
    publication_text_end_sample TEXT DEFAULT '',
    
    tone_of_voice TEXT[] DEFAULT '{}',
    brand_rules TEXT[] DEFAULT '{}',
    compliance_rules TEXT[] DEFAULT '{}',
    audience_insights TEXT[] DEFAULT '{}',
    products JSONB[] DEFAULT '{}',
    locale JSONB DEFAULT '{}',
    additional_info TEXT[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
drop_organizations_table = """
DROP TABLE IF EXISTS organizations CASCADE;
"""

create_organization_tables_queries = [
    create_organizations_table
]

drop_queries = [
    drop_organizations_table
]