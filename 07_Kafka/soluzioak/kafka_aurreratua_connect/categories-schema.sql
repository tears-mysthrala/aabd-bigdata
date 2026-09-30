-- categories (PDF 4.1): RETAIL_DBko taula, DataFlow 2-ko 6. kasutik berrerabilia.
CREATE TABLE IF NOT EXISTS categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_department_id INT NOT NULL,
  category_name VARCHAR(45) NOT NULL
);
-- Lab-datuak (sintetikoak, PDFak errenkadak zehaztu gabe):
INSERT INTO categories (category_department_id, category_name) VALUES
  (1, 'Futbola'), (1, 'Saskibaloia'), (2, 'Ordenagailuak'),
  (2, 'Telefonoak'), (3, 'Liburuak');
