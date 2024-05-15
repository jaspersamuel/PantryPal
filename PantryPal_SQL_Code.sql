CREATE TABLE customers (
    cus_id INT PRIMARY KEY,
    cus_first_name NVARCHAR(30),
    cus_last_name NVARCHAR(30),
    cus_email NVARCHAR(50),
    cus_phone_number BIGINT,
    cus_dob DATE,
    password NVARCHAR(20),
    sign_up_date DATE,
    cus_height FLOAT,
    cus_weight FLOAT,
    cus_diet NVARCHAR(30),
    cus_physical_goal NVARCHAR(30)
);

CREATE TABLE super_market ( 
    sm_id INT PRIMARY KEY,
    sm_name NVARCHAR(50),
    sm_email NVARCHAR(50)
);

CREATE TABLE product_type (
    product_type_id NVARCHAR(50) PRIMARY KEY,
    product_name NVARCHAR(50),
    product_category NVARCHAR(50),
    product_storage NVARCHAR(30)
);

CREATE TABLE products (
    product_id NVARCHAR(50) PRIMARY KEY,
    product_type_id NVARCHAR(50),
    sm_id INT,
    product_brand NVARCHAR(30),
    product_ingredients NVARCHAR(20),
    product_price NVARCHAR(20),
    manufacture_date DATE,
    expiry_date DATE,
    FOREIGN KEY (product_type_id) REFERENCES product_type(product_type_id),
    FOREIGN KEY (sm_id) REFERENCES super_market(sm_id)
);

CREATE TABLE orders (
    order_id NVARCHAR(50),
    product_id NVARCHAR(50),
    cus_id INT,
    cus_sm_membership_id NVARCHAR(50),
    purchase_date DATE,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (cus_id) REFERENCES customers(cus_id),
    FOREIGN KEY (cus_sm_membership_id) REFERENCES super_customer_data(cus_sm_membership_id)
);
CREATE TABLE super_customer_data (
    cus_sm_membership_id NVARCHAR(50) PRIMARY KEY NOT NULL,
    cus_id INT,
    sm_id INT,
    FOREIGN KEY (cus_id) REFERENCES customers(cus_id),
    FOREIGN KEY (sm_id) REFERENCES super_market(sm_id)
);


