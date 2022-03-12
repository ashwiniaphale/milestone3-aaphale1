/* eslint-disable no-alert */
/* eslint-disable react/button-has-type */
/* eslint-disable react/jsx-filename-extension */
/* eslint-disable no-shadow */
/* eslint-disable padded-blocks */
/* eslint-disable arrow-parens */
/* eslint-disable camelcase */
/* eslint-disable quote-props */
/* eslint-disable arrow-body-style */
/* eslint-disable comma-dangle */
/* eslint-disable react/react-in-jsx-scope */
import './App.css';
import { useState, useEffect } from 'react';

function App() {

  const [list_all_comments, setComment] = useState([]);

  useEffect(() => {
    fetch('/reviewfromdb').then(response => response.json()).then(data => {
      setComment(data);
    });
  }, []);

  function deleteReview(id) {
    const newRatings = list_all_comments.filter(list_all_comments => list_all_comments.id !== id);
    setComment(newRatings);
  }

  function saveAllChanges(request) {
    fetch('/reviewfromid', {
      method: 'POST',
      headers: {
        'content_type': 'application/json',
      },
      body: JSON.stringify(request)
    }).then((response) => { return response.json(); });
    alert('Your changes were saved.');
  }

  return (
    <div className="App">
      <center>
        <h2>Your reviews:</h2>
        <table>
          {list_all_comments && list_all_comments.map((list_all_comments) => (
            <tr key={list_all_comments.id}>
              <tb>
                <b>
                  Movie ID:
                  {list_all_comments.movie_id}
                </b>
              </tb>
              &nbsp;
              <tb><input type="text" defaultValue={list_all_comments.rating} /></tb>
              {' '}
              &nbsp;
              <tb><input type="text" defaultValue={list_all_comments.reviews} /></tb>
              &nbsp;
              <button onClick={() => deleteReview(list_all_comments.id)}>Delete</button>
            </tr>
          ))}
        </table>
        <button onClick={() => saveAllChanges(list_all_comments)}>Save All Changes</button>
      </center>
    </div>
  );
}
export default App;
