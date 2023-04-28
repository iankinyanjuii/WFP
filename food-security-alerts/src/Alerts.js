import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      const response = await axios.get('/api/alerts');
      setAlerts(response.data);
    };

    fetchAlerts();
  }, []);

  return (
    <div>
      {/* Render alerts here */}
    </div>
  );
}

export default Alerts;
