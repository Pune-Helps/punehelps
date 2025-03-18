-- Create the Categories table
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add categories for hyperlocal help
INSERT INTO category (name, description, icon) VALUES
-- Emergency Services
('Medical Emergency', 'Urgent medical assistance or ambulance services', 'medical'),
('Fire Emergency', 'Fire-related emergencies or rescue', 'fire'),
('Police Assistance', 'Law enforcement or security concerns', 'police'),
('Disaster Relief', 'Help during floods, earthquakes or other natural disasters', 'disaster'),

-- Daily Needs
('Grocery Delivery', 'Help with grocery shopping or delivery', 'grocery'),
('Medicine Delivery', 'Pickup or delivery of prescription medications', 'medicine'),
('Meal Assistance', 'Prepared meals or food supplies', 'food'),
('Water Supply', 'Drinking water or water delivery services', 'water'),

-- Transportation
('Emergency Transport', 'Urgent transportation to hospital or shelter', 'ambulance'),
('Ride Sharing', 'Shared rides for local commuting', 'car'),
('Senior Transportation', 'Transportation services for elderly', 'elderly'),
('School Transportation', 'Help with school pickup/dropoff', 'school'),

-- Home Services
('Plumbing Issues', 'Help with water leaks or plumbing emergencies', 'plumbing'),
('Electrical Problems', 'Assistance with power outages or electrical issues', 'electrical'),
('Household Repairs', 'General home maintenance and repairs', 'tools'),
('Pest Control', 'Help with pest or insect issues', 'pest'),

-- Care Services
('Childcare', 'Temporary childcare or babysitting', 'child'),
('Elder Care', 'Assistance for senior citizens', 'elderly'),
('Pet Care', 'Pet sitting, walking, or emergency vet transport', 'pet'),
('Patient Care', 'Home care for patients or disabled individuals', 'healthcare'),

-- Community Support
('Language Translation', 'Help with translation or interpretation', 'language'),
('Document Assistance', 'Help with filling forms or applications', 'document'),
('Tech Support', 'Help with computers, phones or internet issues', 'tech'),
('Tutoring', 'Educational support or homework help', 'education'),

-- Professional Services
('Legal Advice', 'Basic legal guidance or referrals', 'legal'),
('Financial Guidance', 'Help with budgeting or financial literacy', 'finance'),
('Job Search', 'Employment leads or resume assistance', 'job'),
('Housing Search', 'Help finding temporary or permanent housing', 'house'),

-- Mental Health
('Counseling', 'Mental health support or counseling', 'counseling'),
('Addiction Support', 'Resources for addiction recovery', 'addiction'),
('Grief Support', 'Support for those experiencing loss', 'grief'),
('Stress Management', 'Help with anxiety or stress reduction', 'stress'),

-- Neighborhood Services
('Snow Removal', 'Help clearing snow from driveways or walkways', 'snow'),
('Lawn Care', 'Assistance with lawn mowing or gardening', 'lawn'),
('Security Watch', 'Neighborhood watch or security monitoring', 'security'),
('Lost & Found', 'Help with lost items or pets', 'search'),

-- Special Needs
('Disability Support', 'Assistance for people with disabilities', 'disability'),
('Mobility Assistance', 'Help with mobility or accessibility issues', 'wheelchair'),
('Special Diet Meals', 'Meals for specific dietary requirements', 'diet'),
('Medical Equipment', 'Sharing or borrowing medical equipment', 'equipment'),

-- Miscellaneous
('Other', 'Any other assistance not listed', 'other');

-- Alter the Listing table to use category_id instead of category string
ALTER TABLE listing
ADD COLUMN category_id INT,
ADD CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES category(id);

-- Migrate existing data
UPDATE listing l
JOIN category c ON l.category = c.name
SET l.category_id = c.id;

-- For any categories that don't match, set them to 'Other'
UPDATE listing
SET category_id = (SELECT id FROM category WHERE name = 'Other')
WHERE category_id IS NULL;

-- Once data is migrated, we can make category_id NOT NULL
ALTER TABLE listing
MODIFY COLUMN category_id INT NOT NULL;

-- Optionally, we can remove the old category column after ensuring data is migrated correctly
-- ALTER TABLE listing DROP COLUMN category;
-- Keep other_category column for now as it might still be useful
