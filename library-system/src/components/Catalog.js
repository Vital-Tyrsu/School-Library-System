import { useState, useEffect } from 'react';

function Catalog() {
  const [searchTerm, setSearchTerm] = useState('');
  const [books, setBooks] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/books/')
      .then((response) => response.json())
      .then((data) => setBooks(data))
      .catch((error) => console.error('Error fetching books:', error));
  }, []);

  const filteredBooks = books.filter(
    (book) =>
      book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      book.author.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleBorrow = (bookId) => {
    console.log(`Borrowing book with ID: ${bookId}`);
    // Later: POST to /api/borrowing/
  };

  return (
    <div className="mt-4">
      <h2>Book Catalog</h2>
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Search by title or author..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {filteredBooks.map((book) => (
            <tr key={book.id}>
              <td>{book.title}</td>
              <td>{book.author}</td>
              <td>{book.status}</td>
              <td>
                {book.status === 'Available' ? (
                  <button
                    className="btn btn-success btn-sm"
                    onClick={() => handleBorrow(book.id)}
                  >
                    Borrow
                  </button>
                ) : (
                  <button className="btn btn-secondary btn-sm" disabled>
                    Unavailable
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Catalog;