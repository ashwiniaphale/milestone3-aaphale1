import './App.css';
import { useState, useEffect } from 'react';

function App() {

  const [list_all_comments, setComment] = useState([]);

  useEffect(() => {
    fetch("/reviewfromdb", { method: "POST" })
      .then((response) => response.json()
        .then(data => { setComment(data.list_all_comments); })
      );
  }, [setComment])

  function deleteReview(id) {
    const newReview = list_all_comments.filter((list_all_comments) => list_all_comments !== id);
    console.log(newReview)
    setComment(newReview);
  }

  return (
    <div className="App">
      <center>
        <h2>Your reviews:</h2>
        <table>
          {list_all_comments && list_all_comments.map((list_all_comments) =>
            <tr>
              <tb><b>Movie ID: {list_all_comments.movie_id}</b></tb>&nbsp;
              <tb><input type="text" defaultValue={list_all_comments.rating}></input></tb> &nbsp;
              <tb><input type="text" defaultValue={list_all_comments.reviews}></input></tb>&nbsp;
              <button onClick={() => deleteReview(list_all_comments)}>Delete</button>
            </tr>
          )}
        </table>
        <button>Save Changes</button>
      </center>
    </div >
  );
}
export default App;
