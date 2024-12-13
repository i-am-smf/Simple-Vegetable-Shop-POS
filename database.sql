CREATE TABLE IF NOT EXISTS Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) DEFAULT 'VEG',
    regional_name VARCHAR(100) DEFAULT 'காய்கறி',
    description VARCHAR(255) DEFAULT NULL,
    cost DECIMAL(10, 2) NOT NULL DEFAULT 1.00, -- Two decimals, default 1.0
    mrp DECIMAL(10, 2) NOT NULL DEFAULT 1.00,  -- Two decimals, default 1.0
    rate DECIMAL(10, 2) NOT NULL DEFAULT 1.00, -- Two decimals, default 1.0
    stock_quantity DECIMAL(10, 3) NOT NULL DEFAULT 0.000, -- Quantity in kilograms
    reorder_level DECIMAL(10, 3) NOT NULL DEFAULT 0.000,  -- Minimum reorder level in kilograms
    added_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Auto-updates on changes
);

CREATE TABLE IF NOT EXISTS Sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00, -- Total amount of the sale
    discount DECIMAL(10, 2) DEFAULT 0.00,             -- Discount applied to the sale
    net_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,  -- Net amount after discount
    sale_items JSON NOT NULL  -- JSON column (handled by Python)
);
