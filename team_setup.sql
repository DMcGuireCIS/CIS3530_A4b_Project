-- A1 Authentication Table
CREATE TABLE app_user (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin','viewer'))
);

-- Index for employee name to speed up name searches
CREATE INDEX IF NOT EXISTS idx_employee_name ON Employee (Lname, Fname);

-- Index for project number to speed up filters or groups based on it
CREATE INDEX IF NOT EXISTS idx_workson_pno ON Works_On (Pno);

-- Added admin user for marking, testing, and debugging
INSERT INTO app_user (username, password_hash, role)
VALUES ('admin', 'scrypt:32768:8:1$ssF0s4lz2AbjM3Oo$0cb71c9ef50a6b03c63e2a1b099abfa6e5b0a26e70d6df4651166e0d84ba2aadad07901b57e25f5e586dff21438b881b55151af6d373d7427fd6109e698a1a82', 'admin')
ON CONFLICT (username) DO NOTHING;