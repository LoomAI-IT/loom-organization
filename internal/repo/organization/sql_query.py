create_organization = """
INSERT INTO organizations (
    name,
    autoposting_moderation,
    publication_text_end_sample,
    video_cut_description_end_sample
)
VALUES (
    :name,
    :autoposting_moderation,
    '',
    ''
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

top_up_balance = """
UPDATE organizations 
SET rub_balance = rub_balance + :amount_rub
WHERE id = :organization_id;
"""

debit_balance = """
UPDATE organizations 
SET rub_balance = rub_balance - :amount_rub
WHERE id = :organization_id 
  AND rub_balance >= :amount_rub;
"""