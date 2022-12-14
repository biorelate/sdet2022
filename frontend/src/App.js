import React from "react";
import { useState, useEffect } from "react";


// App
const App = () => {
  const [documents, setDocuments] = useState([]);
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(2);

  const baseUrl = "http://localhost:5000";

  const get_documents = async (skip, limit) => {
    const response = await fetch(`${baseUrl}/document?skip=${skip}&limit=${limit}`);
    const data = await response.json();
    return data;
  };

  useEffect(() => {
    const fetchData = async () => {
      const documents = await get_documents(skip, limit);
      setDocuments(documents);
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Document List</h1>
      <p>Showing {documents.length} documents</p>
      <p>Showing {skip} to {skip + limit} documents</p>
      <button onClick={() => setSkip(skip - limit)}>Previous</button>
      <button onClick={() => setSkip(skip + limit)}>Next</button>
      <ul>
        {documents.map((document) => (
          <li key={document.doc_id}>
            <h2>{document.title}</h2>
            <p>{document.date}</p>
            <a href={document.url}>{document.url}</a>
            <p>Author: {document.author}</p>
            <p>Concepts: {document.concept1}, {document.concept2}</p>
          </li>
        ))}
      </ul>

    </div>
  );
};

export default App;
