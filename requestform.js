// Card.js
import React, { useState } from 'react';

const Card = ({ title, content }) => {
  const [expanded, setExpanded] = useState(false);

  const handleClick = () => setExpanded(!expanded);

  return (
    <div className="card">
      <div className="card-header">
        <h2>{title}</h2>
        <button onClick={handleClick}>{expanded ? 'Close' : 'Expand'}</button>
      </div>
      {expanded && <div className="card-content"><p>{content}</p></div>}
    </div>
  );
};

export default Card;