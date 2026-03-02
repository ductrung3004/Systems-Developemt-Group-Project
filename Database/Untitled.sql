CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    account_status ENUM('Active','Inactive') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
CREATE TABLE locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    address VARCHAR(255)
);
CREATE TABLE administrators (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
CREATE TABLE managers (
    manager_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
CREATE TABLE maintenance_staff (
    maintenance_staff_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location_id INT NOT NULL,
    hire_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
CREATE TABLE financial_managers (
    finance_manager_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location_id INT NOT NULL,
    hire_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
CREATE TABLE tenants (
    tenant_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ni_number VARCHAR(20) NOT NULL UNIQUE,
    occupation VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
CREATE TABLE apartment_requirements (
    requirement_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL,
    bedrooms INT,
    bathrooms INT,
    furnished BOOLEAN,
    additional_notes TEXT,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);
CREATE TABLE tenant_references (
    reference_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL,
    reference_name VARCHAR(100) NOT NULL,
    relationship_type VARCHAR(50),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);
CREATE TABLE apartments (
    apartment_id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT NOT NULL,
    apartment_number VARCHAR(20),
    bedrooms INT,
    bathrooms INT,
    rent DECIMAL(10,2),
    status ENUM('Available','Occupied','Maintenance') DEFAULT 'Available',
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);
CREATE TABLE lease_agreements (
    lease_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL,
    apartment_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    monthly_rent DECIMAL(10,2),
    status ENUM('Active','Expired','Terminated') DEFAULT 'Active',
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
    FOREIGN KEY (apartment_id) REFERENCES apartments(apartment_id)
);
CREATE TABLE maintenance_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL,
    apartment_id INT NOT NULL,
    description TEXT NOT NULL,
    status ENUM('Pending','In Progress','Resolved') DEFAULT 'Pending',
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_to INT,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
    FOREIGN KEY (apartment_id) REFERENCES apartments(apartment_id),
    FOREIGN KEY (assigned_to) REFERENCES maintenance_staff(maintenance_staff_id)
);
CREATE TABLE complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL,
    description TEXT NOT NULL,
    status ENUM('Open','Closed') DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id)
);
CREATE TABLE invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    tenant_id INT NOT NULL,
    lease_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    issue_date DATE,
    due_date DATE,
    status ENUM('Unpaid','Paid','Late') DEFAULT 'Unpaid',
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
    FOREIGN KEY (lease_id) REFERENCES lease_agreements(lease_id)
);
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT NOT NULL,
    processed_by INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE,
    method VARCHAR(50),
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id),
    FOREIGN KEY (processed_by) REFERENCES financial_managers(finance_manager_id)
);
CREATE TABLE financial_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    generated_by INT NOT NULL,
    report_type VARCHAR(50),
    period_start DATE,
    period_end DATE,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (generated_by) REFERENCES financial_managers(finance_manager_id)
);
