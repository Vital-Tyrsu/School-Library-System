import { useState } from 'react';

function AdminDashboard() {
  const [newBook, setNewBook] = useState({ title: '', author: '' });

  const handleAddBook = (e) => {
    e.preventDefault();
    console.log('Adding book:', newBook);
    // Later: Send API request to add book to database
    setNewBook({ title: '', author: '' });
  };

  return (
    <div className="mt-4">
      <h2>Admin Dashboard</h2>
      <h4>Add New Book</h4>
      <form onSubmit={handleAddBook}>
        <div className="mb-3">
          <label>Title:</label>
          <input
            type="text"
            className="form-control"
            value={newBook.title}
            onChange={(e) => setNewBook({ ...newBook, title: e.target.value })}
            required
          />
        </div>
        <div className="mb-3">
          <label>Author:</label>
          <input
            type="text"
            className="form-control"
            value={newBook.author}
            onChange={(e) => setNewBook({ ...newBook, author: e.target.value })}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">Add Book</button>
      </form>
    </div>
  );
}

export default AdminDashboard;