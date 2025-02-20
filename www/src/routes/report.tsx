import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import axios from "axios";

const client = axios.create({
  baseURL: `http://${import.meta.env.VITE_GIT_RANK_API_URL}`,
  headers: {
    "Content-type": "application/json",
  },
})


export default function Report() {
  const [username, setUsername] = useState('');
  const [shouldFetch, setShouldFetch] = useState(false);

  const { isLoading, isError, isSuccess, data, error }= useQuery({
    queryKey: ['status', username],
    queryFn: async () => {
      const response = await client.get(`/rank/${username}`);
      return response.data;
    },
    enabled: shouldFetch
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setShouldFetch(true);
  };

  return (
    <div>
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="username">
          Insert username:
        </label>
        <input
          id="username"
          type="text"
          className="form-control"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>

      <button 
        type="submit"
        className="btn btn-primary"
        disabled={isLoading}
      >
        {isLoading ? 'Generating report...' : 'Get report'}
      </button>
    </form>

    {isSuccess && (
      <div>
        Report: {JSON.stringify(data, null, 2)}
      </div>
    )}

    {isError && (
      <div>
        Error while getting report: {error.message}
        <br/>
        {error.stack}
      </div>
    )}
  </div>
  );
}
