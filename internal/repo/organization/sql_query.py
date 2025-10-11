create_organization = """
INSERT INTO organizations (
    name
)
VALUES (
    :name
)
RETURNING id;
"""

get_organization_by_id = """
SELECT * FROM organizations
WHERE id = :organization_id;
"""

get_all_organizations = """
SELECT * FROM organizations
ORDER BY created_at DESC;
"""

delete_organization = """
DELETE FROM organizations
WHERE id = :organization_id;
"""

update_balance = """
UPDATE organizations
SET rub_balance = :rub_balance
WHERE id = :organization_id;
"""

# Cost Multipliers queries
create_cost_multiplier = """
INSERT INTO cost_multipliers (
    organization_id,
    generate_text_cost_multiplier,
    generate_image_cost_multiplier,
    generate_vizard_video_cut_cost_multiplier
)
VALUES (
    :organization_id,
    :generate_text_cost_multiplier,
    :generate_image_cost_multiplier,
    :generate_vizard_video_cut_cost_multiplier
)
RETURNING id;
"""

get_cost_multiplier_by_organization_id = """
SELECT * FROM cost_multipliers
WHERE organization_id = :organization_id;
"""

delete_cost_multiplier = """
DELETE FROM cost_multipliers
WHERE organization_id = :organization_id;
"""
