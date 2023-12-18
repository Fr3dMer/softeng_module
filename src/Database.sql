CREATE TABLE `Patients` (
  `Patient_id` integer PRIMARY KEY,
  `Name` varchar(255),
  `DOB` date
);

CREATE TABLE `Samples` (
  `Sample_id` integer PRIMARY KEY,
  `Patient_id` integer,
  `Unique_panel_id` varchar(255),
  `Date` date
);

CREATE TABLE `Panels` (
  `Unique_panel_id` varchar(255) PRIMARY KEY,
  `R_code` varchar(255),
  `Version` integer,
  `gene_info` text
);

ALTER TABLE `Samples` ADD FOREIGN KEY (`Sample_id`) REFERENCES `Patients` (`Patient_id`);

ALTER TABLE `Samples` ADD FOREIGN KEY (`Unique_panel_id`) REFERENCES `Panels` (`Unique_panel_id`);
