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
