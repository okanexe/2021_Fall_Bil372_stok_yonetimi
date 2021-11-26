-- -------------------------------------------------------------
-- TablePlus 4.5.0(396)
--
-- https://tableplus.com/
--
-- Database: guru99
-- Generation Time: 2021-11-26 22:12:00.5780
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."address" (
    "addressid" int4 NOT NULL,
    "country_name" varchar(50),
    "town_name" varchar(50),
    "district_name" varchar(50),
    "apartment_no" int4,
    PRIMARY KEY ("addressid")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."beverage" (
    "productid" int4 NOT NULL,
    "product_name" varchar(100),
    "price" float8,
    "expiration_date" date,
    "category_id" int4,
    "kdv" int4,
    "quantity_lt" float8
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."branch" (
    "branchid" int4 NOT NULL,
    "branch_name" varchar(100),
    "address_id" int4,
    "capacity" int4,
    PRIMARY KEY ("branchid")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."butcher" (
    "productid" int4 NOT NULL,
    "product_name" varchar(100),
    "price" float8,
    "expiration_date" date,
    "category_id" int4,
    "kdv" int4,
    "quantity_kg" float8
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."cleaning" (
    "productid" int4 NOT NULL,
    "product_name" varchar(100),
    "price" float8,
    "expiration_date" date,
    "category_id" int4,
    "kdv" int4,
    "clean_type" varchar(50)
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."container" (
    "containerid" int4 NOT NULL,
    "product_id" int4,
    "weight" float8,
    PRIMARY KEY ("containerid")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."delivery" (
    "deliveryid" int4 NOT NULL,
    "store_id" int4,
    "branch_id" int4,
    "vehicle_id" int4,
    PRIMARY KEY ("deliveryid")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."driver" (
    "driverid" int4 NOT NULL,
    "driver_name" varchar(100),
    "vehicle_id" int4,
    "driver_licence" varchar(100),
    PRIMARY KEY ("driverid")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."manager" (
    "ssn" varchar(100) NOT NULL,
    "personal_name" varchar(100),
    "job_title" varchar(100),
    "email" varchar(100),
    "phone_number" varchar(50),
    "branch_id" int4
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."personal" (
    "ssn" varchar(100) NOT NULL,
    "personal_name" varchar(100),
    "job_title" varchar(100),
    "email" varchar(100),
    "phone_number" varchar(50),
    PRIMARY KEY ("ssn")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."product" (
    "productid" int4 NOT NULL,
    "product_name" varchar(100),
    "price" float8,
    "expiration_date" date,
    "category_id" int4,
    "kdv" int4,
    PRIMARY KEY ("productid")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."product_demand" (
    "demandid" int4 NOT NULL,
    "description" varchar(250),
    "product_id" int4,
    "product_quantity" int4,
    "store_id" int4,
    "branch_id" int4,
    PRIMARY KEY ("demandid")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."sales_consultant" (
    "ssn" varchar(100) NOT NULL,
    "personal_name" varchar(100),
    "job_title" varchar(100),
    "email" varchar(100),
    "phone_number" varchar(50),
    "branch_id" int4
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."store" (
    "storeid" int4 NOT NULL,
    "address_id" int4,
    "store_name" varchar(100),
    "product_id" int4,
    "product_quantity" int4,
    PRIMARY KEY ("storeid")
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."store_personal" (
    "ssn" varchar(100) NOT NULL,
    "personal_name" varchar(100),
    "job_title" varchar(100),
    "email" varchar(100),
    "phone_number" varchar(50),
    "store_id" int4
);

-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Table Definition
CREATE TABLE "public"."vehicle" (
    "vehicleid" int4 NOT NULL,
    "plate" varchar(50),
    "chassis_no" varchar(100),
    "container_id" int4,
    PRIMARY KEY ("vehicleid")
);

INSERT INTO "public"."address" ("addressid", "country_name", "town_name", "district_name", "apartment_no") VALUES
(1, 'ankara', 'çankaya', 'dikmen', 15);

INSERT INTO "public"."branch" ("branchid", "branch_name", "address_id", "capacity") VALUES
(1, 'ÇANKAYA ŞUBE', 1, 100);

INSERT INTO "public"."personal" ("ssn", "personal_name", "job_title", "email", "phone_number") VALUES
('111111', 'okans', 'mühendis', 'okanzshn@gmail.com', '12345678'),
('123', 'ahmet', 'mühendis', 'okanzshn@gmail.com', '12345678');

INSERT INTO "public"."product" ("productid", "product_name", "price", "expiration_date", "category_id", "kdv") VALUES
(1, 'biskrem', 1, '2021-12-26', 1, 0);

ALTER TABLE "public"."branch" ADD FOREIGN KEY ("address_id") REFERENCES "public"."address"("addressid");
ALTER TABLE "public"."container" ADD FOREIGN KEY ("product_id") REFERENCES "public"."product"("productid");
ALTER TABLE "public"."delivery" ADD FOREIGN KEY ("store_id") REFERENCES "public"."store"("storeid");
ALTER TABLE "public"."delivery" ADD FOREIGN KEY ("vehicle_id") REFERENCES "public"."vehicle"("vehicleid");
ALTER TABLE "public"."delivery" ADD FOREIGN KEY ("branch_id") REFERENCES "public"."branch"("branchid");
ALTER TABLE "public"."driver" ADD FOREIGN KEY ("vehicle_id") REFERENCES "public"."vehicle"("vehicleid");
ALTER TABLE "public"."manager" ADD FOREIGN KEY ("branch_id") REFERENCES "public"."branch"("branchid");
ALTER TABLE "public"."product_demand" ADD FOREIGN KEY ("branch_id") REFERENCES "public"."branch"("branchid");
ALTER TABLE "public"."product_demand" ADD FOREIGN KEY ("product_id") REFERENCES "public"."product"("productid");
ALTER TABLE "public"."product_demand" ADD FOREIGN KEY ("store_id") REFERENCES "public"."store"("storeid");
ALTER TABLE "public"."sales_consultant" ADD FOREIGN KEY ("branch_id") REFERENCES "public"."branch"("branchid");
ALTER TABLE "public"."store" ADD FOREIGN KEY ("product_id") REFERENCES "public"."product"("productid");
ALTER TABLE "public"."store" ADD FOREIGN KEY ("address_id") REFERENCES "public"."address"("addressid");
ALTER TABLE "public"."store_personal" ADD FOREIGN KEY ("store_id") REFERENCES "public"."store"("storeid");
ALTER TABLE "public"."vehicle" ADD FOREIGN KEY ("container_id") REFERENCES "public"."container"("containerid");
