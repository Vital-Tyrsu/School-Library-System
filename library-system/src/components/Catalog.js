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
    // For now, assume a student ID (we’ll handle authentication later)
    fetch(`http://127.0.0.1:8000/api/books/${bookId}/borrow/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: 1, due_date: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Book borrowed:', data);
        // Refresh books list
        fetch('http://127.0.0.1:8000/api/books/')
          .then((response) => response.json())
          .then((newData) => setBooks(newData))
          .catch((error) => console.error('Error refreshing books:', error));
      })
      .catch((error) => console.error('Error borrowing book:', error));
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