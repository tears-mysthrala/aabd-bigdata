-- Transcribed from PDF p. 60. Applied once, when the MySQL volume is empty.
USE retail_db;
CREATE TABLE categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_department_id INT NOT NULL,
  category_name VARCHAR(45) NOT NULL
);
INSERT INTO categories (category_department_id, category_name) VALUES
  (1, 'Football'), (2, 'Basketball'), (3, 'Running');
