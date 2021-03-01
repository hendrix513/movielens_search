import React, { Component } from 'react';

class App extends Component {
  constructor(props) {
    super(props);
    this.query_args = {'limit': 10, 'page': 1};
  }
  render() {
    return (
      <form onSubmit={this.mySubmitHandler}>
      <h1>Hello </h1>
      <pre>state = {JSON.stringify(this.state, undefined, '  ')}</pre>
      <p>Movie Title:</p>
      <input
        type='text'
        name='title'
        onChange={this.myChangeHandler}
      />
      <p>Movie tag:</p>
      <input
        type='text'
        name='tag'
        onChange={this.myChangeHandler}
      />
      <p>Movie genre:</p>
      <input
        type='text'
        name='genre'
        onChange={this.myChangeHandler}
      />
      <p>Rating user id:</p>
      <input
        type='number'
        name='rating_user_id'
        onChange={this.myChangeHandler}
      />
      <p>Tag user id:</p>
      <input
        type='number'
        name='tag_user_id'
        onChange={this.myChangeHandler}
      />
      <p>Movie Id:</p>
      <input
        type='number'
        name='movie_id'
        onChange={this.myChangeHandler}
      />
      <p>Results Page:</p>
      <input
        type='number'
        name='page'
        onChange={this.myChangeHandler}
      />
      <input
        type='submit'
      />
      </form>
    );
  }
  myChangeHandler = (event) => {
    let nam = event.target.name;
    let val = event.target.value;
    this.query_args[nam] = val;
  }
  mySubmitHandler = (event) => {
    event.preventDefault();
    fetch('/search_movies?'+ new URLSearchParams(this.query_args).toString()).then((res) => {
      return res.json();
    }).then((res) => {
      console.log(res);
      this.setState({res});
    }).catch((err) => {
      console.log(err);
      this.setState({err});
    });
  }
}

export default App;
