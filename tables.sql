-- Disaster Reports Table
CREATE TABLE IF NOT EXISTS disaster_reports (
    report_id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    disaster_type VARCHAR(50) NOT NULL,
    severity TEXT CHECK (severity IN ('Low', 'Moderate', 'High', 'Severe')),
    description TEXT,
    status VARCHAR(20) DEFAULT 'Active',
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_location ON disaster_reports(location);
CREATE INDEX IF NOT EXISTS idx_disaster_type ON disaster_reports(disaster_type);
CREATE INDEX IF NOT EXISTS idx_report_date ON disaster_reports(report_date);

-- Relief Resources Table
CREATE TABLE IF NOT EXISTS relief_resources (
    resource_id SERIAL PRIMARY KEY,
    resource_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    unit VARCHAR(20) DEFAULT 'units',
    cost_per_unit DECIMAL(10,2) DEFAULT 0.00,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_resource_name ON relief_resources(resource_name);

-- Resource Allocation Table
CREATE TABLE IF NOT EXISTS resource_allocation (
    allocation_id SERIAL PRIMARY KEY,
    report_id INT NOT NULL,
    resource_id INT NOT NULL,
    allocated_quantity INT NOT NULL,
    allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES disaster_reports(report_id) ON DELETE CASCADE,
    FOREIGN KEY (resource_id) REFERENCES relief_resources(resource_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_report_id ON resource_allocation(report_id);
CREATE INDEX IF NOT EXISTS idx_resource_id ON resource_allocation(resource_id);

-- Donations Table
CREATE TABLE IF NOT EXISTS donations (
    donation_id SERIAL PRIMARY KEY,
    donor_name VARCHAR(100) NOT NULL,
    donor_email VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    disaster_id INT,
    message TEXT,
    donation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (disaster_id) REFERENCES disaster_reports(report_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_donor_email ON donations(donor_email);
CREATE INDEX IF NOT EXISTS idx_disaster_id ON donations(disaster_id);
CREATE INDEX IF NOT EXISTS idx_donation_date ON donations(donation_date);

-- Safety Policies Table
CREATE TABLE IF NOT EXISTS safety_policies (
    policy_id SERIAL PRIMARY KEY,
    disaster_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    priority INT DEFAULT 1,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_disaster_type ON safety_policies(disaster_type);
CREATE INDEX IF NOT EXISTS idx_priority ON safety_policies(priority);

-- Disaster News Table
CREATE TABLE IF NOT EXISTS disaster_news (
    news_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    news_type VARCHAR(20) NOT NULL CHECK (news_type IN ('warning', 'prediction', 'update')),
    severity TEXT CHECK (severity IN ('Low', 'Moderate', 'High', 'Severe')),
    location VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    publish_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE disaster_news
ALTER COLUMN severity TYPE TEXT USING severity::TEXT;
ALTER TABLE disaster_news
ALTER COLUMN severity TYPE TEXT USING severity::TEXT;
CREATE INDEX IF NOT EXISTS idx_news_type ON disaster_news(news_type);
CREATE INDEX IF NOT EXISTS idx_severity ON disaster_news(severity);
CREATE INDEX IF NOT EXISTS idx_location ON disaster_news(location);
CREATE INDEX IF NOT EXISTS idx_publish_date ON disaster_news(publish_date);
