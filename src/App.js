import './App.css';
import { useState, useEffect } from 'react';

function App() {

  const [list_all_comments, setComment] = useState([])
  const [delete_comment, deleteComment] = useState([])

  useEffect(() => {
    fetch('/reviewfromdb').then(response => response.json()).then(data => {
      setComment(data.list_all_comments) //grabbing data and passing it through setFact within the useState hook
    })
  }, [])



  return (
    <div>
      <h1> Reviews </h1>
      <center>
        {list_all_comments && list_all_comments.map((list_all_comments) =>
          <ul>
            <p>Movie ID: {list_all_comments.movie_id}</p>
            <p>Rating: {list_all_comments.rating}</p>
            <p>Comments: {list_all_comments.reviews}</p>
          </ul>
        )}
      </center>
    </div>
  );
}
//one_comment => commentBlob(list_all_comments[one_comment]))}
export default App;
