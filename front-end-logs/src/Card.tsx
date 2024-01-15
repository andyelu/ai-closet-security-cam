import { useState, useEffect } from "react";
import axios from "axios";

interface Event {
  id: number;
  time: string;
  image_data: string;
}

function Card() {
  const [events, setEvents] = useState<Event[]>([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/event")
      .then((response) => {
        console.log(response);
        setEvents(response.data.events);
      })
      .catch((error) => {
        console.error("Error fetching data: ", error);
      });
  }, []);

  return (
    <div>
      {events.map((event) => (
        <div className="card" key={event.id}>
          {" "}
          {/* Use event.id for a unique key */}
          <img src={event.image_data} alt={`Event ${event.id}`}></img>
          <h2>{new Date(event.time).toLocaleString()}</h2>{" "}
          {/* Format time as needed */}
        </div>
      ))}
    </div>
  );
}

export default Card;
