
INSERT INTO users (role_id, username, password_hash, first_name, last_name, email, phone_number, occupation, dob, lease_start, lease_end, account_status)
VALUES
(1, 'admin', '$2b$12$/GkJmIu77DCdjqqKrDruoehigf7l6.u6Cmdou2bCCf3K29QQvPQ9.', 'Admin', 'User', 'admin@pams.com', '0700000001', 'Administrator', '1985-02-20', NULL, NULL, 'active'),
(2, 'manager', '$2b$12$RxrBDxXrSq7ug5wd0YteneiePGjT9JdcJHT0adknykODup7LrwFoC', 'Manager', 'User', 'manager@pams.com', '0700000002', 'Property Manager', '1987-04-05', NULL, NULL, 'active'),
(3, 'frontdesk', '$2b$12$7WaUfiy7SclFrEjE7VxiOeH4BYV8X13w0ljMIjyHx1gbASTdEtpWS', 'Front', 'Desk', 'frontdesk@pams.com', '0700000003', 'Front Desk Staff', '1990-05-10', NULL, NULL, 'active'),
(4, 'maintenance', '$2b$12$.rRGPCNvj6cuHZx1ydCuG.pBoBVRVwF9x3fTf00tFwgs4rAz3/z3q', 'Maintenance', 'Staff', 'maintenance@pams.com', '0700000004', 'Maintenance Staff', '1992-07-12', NULL, NULL, 'active'),
(5, 'finance', '$2b$12$7JvvzZTinZ6qd/i0H0LLserOCIAa50dQ6aLweBJx29aTPQyxzw3o2', 'Finance', 'Manager', 'finance@pams.com', '0700000005', 'Finance Manager', '1989-08-15', NULL, NULL, 'active'),
(6, 'tenant', '$2b$12$PR2HtI7Y6GB6IeSdukDkc.FxSU3cOD5Yl6g82JW7c.UfwELyzgWqm', 'Trung', 'Nguyen', 'truntrun@gmail.com', '07932241664', 'Tenant', '1993-03-10', '2026-01-01', '2027-01-01', 'active');
